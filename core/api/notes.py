from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Dict
import json
import database, models, auth
from models.notes import Note
from api.auth import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])

# Schemas
class NoteCreate(BaseModel):
    title: str
    content: str = ""

class NoteUpdate(BaseModel):
    title: str = None
    content: str = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

    class Config:
        from_attributes = True

# CRUD Endpoints
@router.post("/", response_model=NoteResponse)
async def create_note(
    note: NoteCreate, 
    user: models.User = Depends(get_current_user), 
    db: AsyncSession = Depends(database.get_db)
):
    new_note = Note(title=note.title, content=note.content, owner_id=user.id)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return {
        "id": new_note.id, 
        "title": new_note.title, 
        "content": new_note.content, 
        "created_at": str(new_note.created_at)
    }

@router.get("/", response_model=List[NoteResponse])
async def list_notes(
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    query = select(Note).filter(Note.owner_id == user.id)
    result = await db.execute(query)
    notes = result.scalars().all()
    
    return [{
        "id": n.id, 
        "title": n.title, 
        "content": n.content, 
        "created_at": str(n.created_at)
    } for n in notes]

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    query = select(Note).filter(Note.id == note_id, Note.owner_id == user.id)
    result = await db.execute(query)
    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": str(note.created_at)
    }

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: int,
    update: NoteUpdate,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    query = select(Note).filter(Note.id == note_id, Note.owner_id == user.id)
    result = await db.execute(query)
    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if update.title is not None:
        note.title = update.title
    if update.content is not None:
        note.content = update.content
    
    await db.commit()
    await db.refresh(note)
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "created_at": str(note.created_at)
    }

# WebSocket for Collaboration
class NoteConnectionManager:
    def __init__(self):
        # {note_id: [WebSocket]}
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, note_id: int):
        await websocket.accept()
        if note_id not in self.active_connections:
            self.active_connections[note_id] = []
        self.active_connections[note_id].append(websocket)

    def disconnect(self, websocket: WebSocket, note_id: int):
        if note_id in self.active_connections:
            if websocket in self.active_connections[note_id]:
                self.active_connections[note_id].remove(websocket)
            if not self.active_connections[note_id]:
                del self.active_connections[note_id]

    async def broadcast(self, note_id: int, message: dict, exclude: WebSocket = None):
        if note_id in self.active_connections:
            for connection in self.active_connections[note_id]:
                if connection != exclude:
                    await connection.send_text(json.dumps(message))

manager = NoteConnectionManager()

import httpx
import os

NEXT_API_URL = os.getenv("NEXT_PUBLIC_SITE_URL", "http://frontend:3000")

@router.websocket("/ws/{note_id}")
async def websocket_endpoint(websocket: WebSocket, note_id: int, token: str):
    # Verify Better Auth token
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{NEXT_API_URL}/api/auth/get-session",
                headers={"Authorization": f"Bearer {token}"}
            )
            if resp.status_code != 200:
                await websocket.close(code=4001)
                return
        except Exception:
            await websocket.close(code=4001)
            return

    await manager.connect(websocket, note_id)
    try:
        while True:
            data = await websocket.receive_text()
            # In a real collaborative app (Yjs), we would relay binary updates.
            # Here we just relay text/json for a simple "live update" simulation.
            # Client sends: {"content": "new text"}
            # We broadcast to others
            msg = json.loads(data)
            await manager.broadcast(note_id, msg, exclude=websocket)
            
            # Optional: Debounced save to DB could happen here or via API calls from client
    except WebSocketDisconnect:
        manager.disconnect(websocket, note_id)

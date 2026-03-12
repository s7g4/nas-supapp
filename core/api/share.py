from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import uuid
import database, models
from models.filesystem import File
from api.auth import get_current_user

router = APIRouter(prefix="/share", tags=["Share"])

# In-memory store for links (Use Redis/DB in prod)
# {uuid: {"file_id": int, "expires_at": datetime}}
share_links = {}

class ShareRequest(BaseModel):
    file_id: int
    minutes: int = 60

@router.post("/link")
async def create_share_link(
    req: ShareRequest,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    # Verify ownership
    result = await db.execute(select(File).filter(File.id == req.file_id, File.owner_id == user.id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="File not found")
        
    link_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=req.minutes)
    
    share_links[link_id] = {
        "file_id": req.file_id,
        "expires_at": expires_at
    }
    
    return {"url": f"/share/{link_id}", "expires_at": str(expires_at)}

@router.get("/{link_id}")
async def access_share_link(
    link_id: str,
    db: AsyncSession = Depends(database.get_db)
):
    data = share_links.get(link_id)
    if not data:
        raise HTTPException(status_code=404, detail="Link not found")
        
    if datetime.utcnow() > data["expires_at"]:
        del share_links[link_id]
        raise HTTPException(status_code=410, detail="Link expired")
    
    # In real app, redirect to download or stream
    return {"status": "valid", "file_id": data["file_id"]}

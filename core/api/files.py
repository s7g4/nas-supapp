from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
import database, models, auth
from models.filesystem import File, Folder
from api.auth import get_current_user

router = APIRouter(prefix="/files", tags=["Files"])

# Schemas
class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class FileResponse(BaseModel):
    id: int
    name: str
    size: int
    content_type: str
    created_at: str
    is_folder: bool = False

    class Config:
        from_attributes = True

# Endpoints

@router.post("/folders", response_model=FileResponse)
async def create_folder(
    folder: FolderCreate, 
    user: models.User = Depends(get_current_user), 
    db: AsyncSession = Depends(database.get_db)
):
    new_folder = Folder(
        name=folder.name,
        owner_id=user.id,
        parent_id=folder.parent_id
    )
    db.add(new_folder)
    await db.commit()
    await db.refresh(new_folder)
    
    return {
        "id": new_folder.id,
        "name": new_folder.name,
        "size": 0,
        "content_type": "directory",
        "created_at": str(new_folder.created_at),
        "is_folder": True
    }

@router.get("/list", response_model=List[FileResponse])
async def list_files(
    folder_id: Optional[int] = None,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    # Get Folders
    q_folders = select(Folder).filter(Folder.owner_id == user.id, Folder.parent_id == folder_id)
    result_folders = await db.execute(q_folders)
    folders = result_folders.scalars().all()

    # Get Files
    q_files = select(File).filter(File.owner_id == user.id, File.folder_id == folder_id)
    result_files = await db.execute(q_files)
    files = result_files.scalars().all()

    response = []
    
    for f in folders:
        response.append({
             "id": f.id, 
             "name": f.name, 
             "size": 0, 
             "content_type": "directory", 
             "created_at": str(f.created_at),
             "is_folder": True
        })

    for f in files:
        response.append({
             "id": f.id, 
             "name": f.name, 
             "size": f.size, 
             "content_type": f.content_type, 
             "created_at": str(f.created_at),
             "is_folder": False
        })

    return response

@router.post("/upload/init")
async def init_upload(
    name: str, 
    size: int, 
    content_type: str, 
    folder_id: Optional[int] = None,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    # In a real app, we check quota here.
    new_file = File(
        name=name,
        size=size,
        content_type=content_type,
        storage_path=f"{user.id}/{name}", # Simplified path
        owner_id=user.id,
        folder_id=folder_id
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)

    return {"file_id": new_file.id, "path": new_file.storage_path}

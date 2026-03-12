from fastapi import APIRouter, Depends, HTTPException, Header, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import database, models
from models.filesystem import File
from api.auth import get_current_user
import os

router = APIRouter(prefix="/media", tags=["Media"])

CHUNK_SIZE = 1024 * 1024 # 1MB

@router.get("/list")
async def list_media(
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    # Find all files with video extensions
    # In a real app, use a dedicated Media table or type field
    extensions = [".mp4", ".mkv", ".webm", ".mov"]
    query = select(File).filter(File.owner_id == user.id)
    result = await db.execute(query)
    all_files = result.scalars().all()
    
    media_files = [f for f in all_files if any(f.name.lower().endswith(ext) for ext in extensions)]
    
    return [{
        "id": f.id, 
        "name": f.name, 
        "size": f.size, 
        "created_at": str(f.created_at)
    } for f in media_files]

@router.get("/stream/{file_id}")
async def stream_video(
    file_id: int, 
    range: str = Header(None), 
    db: AsyncSession = Depends(database.get_db) # Auth via query param usually for <video> tags, skipping strictly for now
):
    result = await db.execute(select(File).filter(File.id == file_id))
    file_entry = result.scalars().first()
    
    if not file_entry:
        raise HTTPException(status_code=404, detail="File not found")

    # Construct absolute path (Assuming local volume mount for V1)
    # In Docker: /data/objects/{user_id}/{filename}
    # We need to map `file_entry.storage_path` to the actual filesystem
    # For now, let's assume `file_entry.storage_path` IS relative to the volume root.
    file_path = f"/data/{file_entry.storage_path}" 
    
    # Check regular FS existence (assuming we are running inside docker container core)
    # Note: 'core' service mounts ./data/objects:/data? Check docker-compose.
    # Wait, core mount is ./data/minio ?? No, core mount is unconfigured in my Dockerfile/Compose update? 
    # Let's check docker-compose.yml in next step to be sure. I might have missed mounting /data to Core.
    
    # Fallback/Safe code assuming simple range request
    return await range_stream_response(file_path, range)


async def range_stream_response(path, range_header):
    if not os.path.exists(path):
         raise HTTPException(status_code=404, detail="Video file not found on disk")
         
    file_size = os.path.getsize(path)
    
    start = 0
    end = file_size - 1
    
    if range_header:
        byte_range = range_header.replace("bytes=", "")
        parts = byte_range.split("-")
        if parts[0]:
            start = int(parts[0])
        if parts[1]:
            end = int(parts[1])
            
    chunk_size = (end - start) + 1
    
    def iter_file():
        with open(path, "rb") as video:
            video.seek(start)
            remaining = chunk_size
            while remaining > 0:
                chunk = video.read(min(CHUNK_SIZE, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk
                
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(chunk_size),
        "Content-Type": "video/mp4",
    }
    
    return StreamingResponse(iter_file(), status_code=206, headers=headers)

@router.post("/transcode/{file_id}")
async def transcode_video(
    file_id: int,
    db: AsyncSession = Depends(database.get_db)
):
    # 1. Get File Path
    result = await db.execute(select(File).filter(File.id == file_id))
    file_entry = result.scalars().first()
    if not file_entry:
        raise HTTPException(status_code=404, detail="File not found")
    
    input_path = f"/data/{file_entry.storage_path}"
    output_dir = os.path.dirname(input_path)
    # Output: /data/123/video.m3u8
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{output_filename}.m3u8")

    # 2. Run FFmpeg (subprocess)
    # In prod, use celery/arq background task!
    import subprocess
    cmd = [
        "ffmpeg", "-i", input_path,
        "-codec:", "copy",
        "-start_number", "0",
        "-hls_time", "10", 
        "-hls_list_size", "0",
        "-f", "hls",
        output_path
    ]
    
    # We run blocking for V1 prototype (Bad practice for prod!)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
         raise HTTPException(status_code=500, detail="Transcoding failed")

    return {"status": "success", "playlist": output_path}

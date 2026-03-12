from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from api import auth as auth_router
from api import transfer as transfer_router
from api import files as files_router
from api import media as media_router
from api import chat as chat_router
from api import notes as notes_router
from api import search as search_router
from api import share as share_router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown

app = FastAPI(
    title="NAS Super-App Core",
    description="Microkernel-inspired core for the NAS Super-App",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(auth_router.router)
app.include_router(transfer_router.router)
app.include_router(transfer_router.internal_router)
app.include_router(files_router.router)
app.include_router(media_router.router)
app.include_router(chat_router.router)
app.include_router(notes_router.router)
app.include_router(search_router.router)
app.include_router(share_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to NAS Super-App Core (Microkernel) 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "core"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

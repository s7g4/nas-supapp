from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from services import ai

router = APIRouter(prefix="/search", tags=["Search"])

class IndexRequest(BaseModel):
    id: int
    text: str

class SearchResult(BaseModel):
    id: int
    text: str
    score: float

@router.post("/index")
async def index_content(req: IndexRequest):
    ai.add_to_index(req.id, req.text)
    return {"status": "indexed"}

@router.get("/", response_model=List[SearchResult])
async def search(q: str):
    return ai.search_index(q)

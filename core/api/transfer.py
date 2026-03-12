from fastapi import APIRouter, Depends, HTTPException
import schemas, auth, models
from api.auth import get_current_user
import os

router = APIRouter(prefix="/transfer", tags=["Transfer"])
internal_router = APIRouter(prefix="/internal", tags=["Internal"])

QUIC_ADDR = os.getenv("QUIC_PUBLIC_ADDR", "localhost:6666")

@router.post("/prepare", response_model=schemas.TransferTokenResponse)
async def prepare_transfer(req: schemas.TransferPrepareRequest, current_user: models.User = Depends(get_current_user)):
    # In a real app, verify permissions to access 'req.path' here.
    
    token_data = {
        "sub": current_user.email,
        "path": req.path,
        "op": req.operation
    }
    
    transfer_token = auth.create_transfer_token(token_data)
    
    return {
        "transfer_token": transfer_token,
        "quic_addr": QUIC_ADDR,
        "path": req.path,
        "expires_in": auth.TRANSFER_TOKEN_EXPIRE_SECONDS
    }

@internal_router.get("/validate-token")
async def validate_token(token: str):
    # This endpoint is called by the Go Transfer Engine
    payload = auth.decode_token(token)
    if not payload or payload.get("type") != "transfer":
        raise HTTPException(status_code=401, detail="Invalid transfer token")
    
    return {
        "valid": True,
        "user": payload.get("sub"),
        "path": payload.get("path"),
        "op": payload.get("op")
    }

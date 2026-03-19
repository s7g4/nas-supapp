from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import database, models, auth
from models.filesystem import File, Folder
from sqlalchemy.future import select

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

import httpx
import os

NEXT_API_URL = os.getenv("NEXT_PUBLIC_SITE_URL", "http://frontend:3000")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate the session with Better Auth running on Next.js
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{NEXT_API_URL}/api/auth/get-session",
                headers={"Authorization": f"Bearer {token}"}
            )
            if resp.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid session",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            data = resp.json()
            user_data = data.get("user")
            if not user_data:
                raise HTTPException(status_code=401, detail="User data missing")
                
            # Create a mock user object or use dict depending on need.
            # We will return the dictionary representing the user from Better Auth.
            return models.User(
                id=user_data.get("id"),
                email=user_data.get("email"),
                full_name=user_data.get("name"),
            )
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Auth server unavailable")

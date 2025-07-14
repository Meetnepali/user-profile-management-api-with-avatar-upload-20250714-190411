from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.auth import get_current_user
from app.models import User, get_async_session
from app.schemas import UserProfileUpdate, UserProfileResponse
from app.storage import save_avatar_async, get_avatar_path
from app.exceptions import register_exception_handlers
from typing import Optional
import os
import shutil

app = FastAPI()

register_exception_handlers(app)

@app.put("/profile", response_model=UserProfileResponse,
         summary="Update your display name and bio", tags=["Profile"])
async def update_profile(
    updates: UserProfileUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    user.display_name = updates.display_name
    user.bio = updates.bio
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserProfileResponse.from_orm(user)

@app.post("/profile/avatar", summary="Upload profile avatar", tags=["Profile"])
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    avatar_url = await save_avatar_async(user.id, file)
    user.avatar_url = avatar_url
    db.add(user)
    await db.commit()
    return {"avatar_url": avatar_url}

@app.get("/profile", response_model=UserProfileResponse,
         summary="Get your profile details", tags=["Profile"])
async def get_my_profile(user: User = Depends(get_current_user)):
    return UserProfileResponse.from_orm(user)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User Profile API",
        version="1.0.0",
        description="Manage user profiles including avatars.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

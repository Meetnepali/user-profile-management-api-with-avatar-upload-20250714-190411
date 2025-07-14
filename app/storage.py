import os
from fastapi import UploadFile, HTTPException, status
import aiofiles
import imghdr
from uuid import uuid4

UPLOAD_DIR = "./avatars"
MAX_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_TYPES = {"jpeg", "png"}

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_avatar_async(user_id: int, file: UploadFile):
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Avatar too large (≤2MB allowed)")
    ext = guess_ext(contents)
    if ext not in {"jpeg", "png"}:
        raise HTTPException(status_code=400, detail="Invalid image type (JPEG/PNG required)")
    filename = f"user_{user_id}_{uuid4().hex}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(path, "wb") as out:
        await out.write(contents)
    # Prevent direct file serving via public web
    return f"/avatars/{filename}"

def guess_ext(contents: bytes):
    fmt = imghdr.what(None, contents)
    if fmt == 'jpeg':
        return 'jpeg'
    if fmt == 'png':
        return 'png'
    return None

def get_avatar_path(avatar_url: str) -> str:
    filename = os.path.basename(avatar_url)
    return os.path.join(UPLOAD_DIR, filename)

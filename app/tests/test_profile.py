import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base, engine
import os
import io
import tempfile

@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Teardown not required for ephemeral test.db

@pytest.mark.anyio
async def test_update_profile():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {"display_name": "Alice Test", "bio": "Hello!"}
        resp = await ac.put("/profile", json=data)
        assert resp.status_code == 200
        body = resp.json()
        assert body['display_name'] == data['display_name']
        assert body['bio'] == data['bio']

@pytest.mark.anyio
async def test_avatar_upload_jpeg():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        image_bytes = b"\xff\xd8\xff" + b"0"*2000  # fake jpeg header
        files = {"file": ("avatar.jpg", image_bytes, "image/jpeg")}
        resp = await ac.post("/profile/avatar", files=files)
        assert resp.status_code == 200
        avatar_url = resp.json()["avatar_url"]
        assert avatar_url.endswith(".jpeg") or avatar_url.endswith(".jpg")

@pytest.mark.anyio
async def test_avatar_type_rejected():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        pdf_bytes = b"%PDF-foobar"
        files = {"file": ("avatar.pdf", pdf_bytes, "application/pdf")}
        resp = await ac.post("/profile/avatar", files=files)
        assert resp.status_code == 400
        assert "Invalid image type" in resp.text

@pytest.mark.anyio
async def test_avatar_size_rejected():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # JPEG header, rest random, size >2MB
        image_bytes = b"\xff\xd8\xff" + b"0"*(2*1024*1024+5)
        files = {"file": ("avatar.jpg", image_bytes, "image/jpeg")}
        resp = await ac.post("/profile/avatar", files=files)
        assert resp.status_code == 413
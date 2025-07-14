from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_async_session():
    async def _get_session():
        async with async_session() as session:
            yield session
    return _get_session

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(32), nullable=False)
    bio = Column(String(160), nullable=True)
    avatar_url = Column(String(256), nullable=True)
    # Password and email fields exist in real systems (omitted for brevity).

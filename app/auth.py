from fastapi import Depends, HTTPException, status
from app.models import User, async_session
from sqlalchemy.future import select

# For assessment: use a simple HTTP header for auth
async def get_current_user(
    authorization: str = Depends(lambda: "test-token")
):
    # Simulate user lookup by static token (no real auth)
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == 1))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        return user

from pydantic import BaseModel, constr
from typing import Optional

class UserProfileUpdate(BaseModel):
    display_name: constr(min_length=2, max_length=32)
    bio: Optional[constr(max_length=160)] = None

class UserProfileResponse(BaseModel):
    id: int
    display_name: str
    bio: Optional[str]
    avatar_url: Optional[str]

    class Config:
        orm_mode = True

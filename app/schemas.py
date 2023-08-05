from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

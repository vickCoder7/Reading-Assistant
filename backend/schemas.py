from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    google_id: str
    title: str
    author: str
    description: Optional[str] = None
    published: bool = True

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserBookBase(BaseModel):
    book_id: int
    status: str
    rating: Optional[int] = None

class UserBookCreate(UserBookBase):
    user_id: int

class UserBookResponse(UserBookBase):
    id: int
    created_at: datetime
    book: BookResponse

    class Config:
        orm_mode = True

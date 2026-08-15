from typing import Optional
from sqlmodel import SQLModel

class BookCreate(SQLModel):
    title: str
    author: str
    category: str
    year: int
    available: bool = True

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    year: Optional[int] = None
    available: Optional[bool] = None

class BookRead(SQLModel):
    id: int
    title: str
    author: str
    category: str
    year: int
    available: bool
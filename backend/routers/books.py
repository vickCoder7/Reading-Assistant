from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db
from services import google_books

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/search", response_model=List[schemas.BookBase])
def search_books(query: str):
    """
    Search for books using the Google Books API.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query string is required")
    
    results = google_books.search_books(query)
    return results

@router.post("/", response_model=schemas.UserBookResponse)
def add_book_to_library(book_data: schemas.BookCreate, user_id: int = 1, db: Session = Depends(get_db)):
    """
    Add a book to the user's library.
    1. Check if book exists in DB. If not, add it.
    2. Create a UserBook entry linking the user to the book.
    """
    # 1. Check/Add Book
    db_book = db.query(models.Book).filter(models.Book.google_id == book_data.google_id).first()
    
    if not db_book:
        db_book = models.Book(**book_data.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    
    # 2. Check/Add UserBook Link
    # Check if already in library
    existing_link = db.query(models.UserBook).filter(
        models.UserBook.user_id == user_id,
        models.UserBook.book_id == db_book.id
    ).first()
    
    if existing_link:
        raise HTTPException(status_code=400, detail="Book already in library")
    
    new_user_book = models.UserBook(
        user_id=user_id,
        book_id=db_book.id,
        status="WANT_TO_READ" # Default status
    )
    db.add(new_user_book)
    db.commit()
    db.refresh(new_user_book)
    
    return new_user_book

@router.get("/", response_model=List[schemas.UserBookResponse])
def get_user_library(user_id: int = 1, db: Session = Depends(get_db)):
    """
    Get all books in the user's library.
    """
    library = db.query(models.UserBook).filter(models.UserBook.user_id == user_id).all()
    return library

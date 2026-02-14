from database import Base
from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey, Float, Text, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text, nullable=True) # Added for AI context
    embedding = Column(PickleType, nullable=True) # Added for recommenders. Ideally use pgvector in prod, Pickle for SQLite
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class UserBook(Base):
    __tablename__ = "user_books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False) # In future, link to a User table
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False) # 'WANT_TO_READ', 'READING', 'FINISHED'
    rating = Column(Integer, nullable=True) # Moved from Book. 1-5 scale
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    book = relationship("Book")
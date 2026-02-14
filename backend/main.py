from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from database import engine
from routers import books

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(books.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Personal Reading Assistant API"}
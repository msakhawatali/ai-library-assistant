from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.models.book import Book 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI Library Assistant API"}


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
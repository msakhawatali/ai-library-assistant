from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.models.book import Book 
from app.api.routers.books import router as books_router
from app.api.routers.ai import router as ai_router
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(books_router, prefix="/api")
app.include_router(ai_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "AI Library Assistant API"}


@app.get("/health")
async def health():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
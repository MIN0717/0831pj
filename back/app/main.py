from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.imageRag.web import router as image_rag_router

from app.auth import router as auth_router
from app.db import Base, engine
import app.models


app = FastAPI(
    title="Image RAG API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# PostgreSQL 테이블 생성
Base.metadata.create_all(bind=engine)


# 기존 Image RAG API
app.include_router(
    image_rag_router
)


# 인증 API
app.include_router(
    auth_router
)


@app.get("/")
def root():
    return {
        "message": "Image RAG API",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }
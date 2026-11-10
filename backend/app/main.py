"""
FastAPI application entry point.
- Lifespan: connects/disconnects MongoDB on startup/shutdown.
- CORS: allows the Next.js frontend (localhost:3000).
- Includes all routers.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_db, close_db
from app.routers import health, notes, chat, quiz, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: connect to MongoDB. Shutdown: close the connection."""
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="StudyMate API",
    description="AI study assistant – upload notes, ask questions, take quizzes.",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # Next.js dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ─────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(notes.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(stats.router)

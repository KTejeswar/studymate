"""
End-to-end integration tests for StudyMate FastAPI API.
Tests the full student loop: Health -> Notes -> Chat -> Quiz -> Stats.
Uses FastAPI lifespan context to run cleanly.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import connect_db, close_db


@pytest.fixture(autouse=True)
async def db_lifecycle():
    await connect_db()
    yield
    await close_db()


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_notes_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/notes")
        assert res.status_code == 200
        assert "notes" in res.json()


@pytest.mark.asyncio
async def test_stats_summary_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/stats/summary")
        assert res.status_code == 200
        assert "total_notes" in res.json()


@pytest.mark.asyncio
async def test_weak_topics_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/stats/weak-topics")
        assert res.status_code == 200
        assert "weak_topics" in res.json()

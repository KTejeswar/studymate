"""
Async MongoDB connection using Motor.
Provides a singleton client and a database reference.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_db() -> None:
    """Open the MongoDB connection and store references."""
    global _client, _db
    _client = AsyncIOMotorClient(settings.mongodb_uri)
    _db = _client[settings.mongodb_db_name]
    # Quick ping to verify the connection works
    await _client.admin.command("ping")
    print(f"✅ Connected to MongoDB: {settings.mongodb_db_name}")


async def close_db() -> None:
    """Close the MongoDB connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        print("🔌 MongoDB connection closed")


def get_db() -> AsyncIOMotorDatabase:
    """Return the database instance. Call after connect_db()."""
    if _db is None:
        raise RuntimeError("Database not connected. Call connect_db() first.")
    return _db

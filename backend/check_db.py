import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def check():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.studymate

    notes_count = await db.notes.count_documents({})
    chunks_count = await db.chunks.count_documents({})

    print("=" * 60)
    print("           StudyMate Database Inspection")
    print("=" * 60)

    # 1. Notes Status
    print(f"\n📂 Total Notes Uploaded: {notes_count}")
    if notes_count > 0:
        async for note in db.notes.find().sort("created_at", -1).limit(5):
            print(f"   • Note: {note.get('filename')} | Subject: {note.get('subject')} | Pages: {note.get('page_count')}")

    # 2. Chunks Status
    print(f"\n🧩 Total Chunks in DB: {chunks_count}")
    if chunks_count > 0:
        chunk = await db.chunks.find_one()
        embedding = chunk.get("embedding", [])
        has_embedding = len(embedding) > 0

        print(f"   • Embedded Status: {'✅ YES' if has_embedding else '❌ NO'}")
        print(f"   • Embedding Dimension: {len(embedding)} numbers")
        print(f"   • Associated File: {chunk.get('filename')}")
        print(f"   • Page: {chunk.get('page')}")
        print(f"   • Sample Chunk Text: '{chunk.get('text', '')[:100]}...'")
    else:
        print("   (No chunks created yet. Upload a note via Swagger or frontend to create chunks!)")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(check())


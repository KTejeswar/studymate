import asyncio
from app.database import connect_db, close_db, get_db
from app.llm import call_embeddings

async def main():
    await connect_db()
    db = get_db()
    
    chunks = await db.chunks.find({}).to_list(length=2000)
    print(f"Total chunks in database to check: {len(chunks)}")
    
    updated = 0
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["text"] for c in batch]
        new_embeddings = await call_embeddings(texts)
        
        for c, emb in zip(batch, new_embeddings):
            await db.chunks.update_one(
                {"_id": c["_id"]},
                {"$set": {"embedding": emb}}
            )
            updated += 1
            
    print(f"✅ SUCCESS! Successfully updated {updated} chunks to current 384-dim embeddings!")
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())

"""
Complete diagnostic script for StudyMate.
Tests MongoDB, Groq, Gemini, and Embeddings independently.
Does NOT modify any files.
"""

import asyncio
from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient

# Load values directly from .env without caching
env = dotenv_values(".env")

groq_key = env.get("GROQ_API_KEY", "").strip('"\'')
gemini_key = env.get("GEMINI_API_KEY", "").strip('"\'')
mongo_uri = env.get("MONGODB_URI", "mongodb://localhost:27017")
mongo_db = env.get("MONGODB_DB_NAME", "studymate")


print("=" * 70)
print("🔍 STUDYMATE SYSTEM DIAGNOSTICS")
print("=" * 70)

# ── 1. MONGODB TEST ──────────────────────────────────────────
print("\n[1/4] TESTING MONGODB CONNECTION...")
try:
    client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=2000)
    asyncio.run(client.admin.command("ping"))
    db = client[mongo_db]
    note_cnt = asyncio.run(db.notes.count_documents({}))
    chunk_cnt = asyncio.run(db.chunks.count_documents({}))
    print(f"  ✅ MongoDB connected successfully to '{mongo_db}'")
    print(f"     • Notes in DB: {note_cnt}")
    print(f"     • Chunks in DB: {chunk_cnt}")
except Exception as e:
    print(f"  ❌ MongoDB Error: {e}")


# ── 2. GROQ TEST ─────────────────────────────────────────────
print("\n[2/4] TESTING GROQ API KEY...")
if not groq_key:
    print("  ⚠️ No GROQ_API_KEY set in .env")
else:
    try:
        from groq import Groq
        groq_client = Groq(api_key=groq_key)
        models = groq_client.models.list()
        all_model_ids = [m.id for m in models.data]
        print(f"  ✅ Groq authenticated successfully!")
        print(f"     Total models accessible: {len(all_model_ids)}")
        
        # Look for usable chat models
        chat_candidates = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ]
        available_chat = [m for m in chat_candidates if m in all_model_ids]
        
        if available_chat:
            test_model = available_chat[0]
            print(f"     Available chat models: {available_chat}")
            print(f"     Testing generation with '{test_model}'...")
            res = groq_client.chat.completions.create(
                model=test_model,
                messages=[{"role": "user", "content": "Respond with: Groq is fully working!"}],
                max_tokens=30,
            )
            print(f"  ✅ GROQ GENERATION SUCCEEDED: '{res.choices[0].message.content.strip()}'")
        else:
            print("     Accessible models on this key:")
            for m in all_model_ids[:10]:
                print(f"       • {m}")
            print("  ⚠️ Notice: This key only has access to guard models, not general chat models.")
    except Exception as e:
        print(f"  ❌ Groq Error: {e}")


# ── 3. GEMINI TEST ───────────────────────────────────────────
print("\n[3/4] TESTING GEMINI API KEY...")
if not gemini_key:
    print("  ⚠️ No GEMINI_API_KEY set in .env")
else:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=gemini_key)
        
        async def test_gemini():
            res = await gemini_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents="Say: Gemini is working!",
            )
            return res.text
            
        text = asyncio.run(test_gemini())
        print(f"  ✅ GEMINI GENERATION SUCCEEDED: '{text.strip()}'")
    except Exception as e:
        print(f"  ❌ Gemini Error Details:")
        print(f"     {e}")


# ── 4. EMBEDDINGS TEST ───────────────────────────────────────
print("\n[4/4] TESTING LOCAL EMBEDDINGS (CPU / Offline Fallback)...")
try:
    from fastembed import TextEmbedding
    model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    vec = list(model.embed(["Hello world"]))[0]
    print(f"  ✅ Local fastembed works! Vector dimension: {len(vec)}")
except Exception as e:
    print(f"  ❌ Local Embeddings Error: {e}")

print("\n" + "=" * 70)

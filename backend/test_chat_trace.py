import asyncio
from app.database import connect_db, close_db
from app.agent.graph import study_agent

async def main():
    await connect_db()
    try:
        print("Testing agent chat with prompt: 'Give a quick 3-bullet revision sheet'...")
        res = await study_agent.ainvoke({
            "question": "Give a quick 3-bullet revision sheet",
            "subject": None,
            "user_id": "demo",
            "rewrite_count": 0,
            "steps_log": [],
        })
        print("✅ SUCCESS! Answer:")
        print(res.get("answer"))
    except Exception as e:
        import traceback
        print("❌ EXACT AGENT ERROR:")
        traceback.print_exc()
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())

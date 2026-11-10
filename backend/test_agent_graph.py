import asyncio
from app.database import connect_db, close_db
from app.agent.graph import study_agent


async def main():
    await connect_db()

    print("=" * 60)
    print("TEST 1: Chit-chat question (should skip retrieval)")
    print("=" * 60)
    out1 = await study_agent.ainvoke({
        "question": "Hello there!",
        "subject": None,
        "user_id": "demo",
        "rewrite_count": 0,
        "steps_log": [],
    })
    print(f"Answer: {out1['answer']}\n")

    print("=" * 60)
    print("TEST 2: Subject question from uploaded notes")
    print("=" * 60)
    out2 = await study_agent.ainvoke({
        "question": "What is Newton's Second Law and its formula?",
        "subject": None,
        "user_id": "demo",
        "rewrite_count": 0,
        "steps_log": [],
    })
    print(f"Answer: {out2['answer']}")
    print(f"Citations: {out2.get('citations')}\n")

    await close_db()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from app.database import connect_db, close_db
from app.services.quiz import generate_quiz

async def main():
    await connect_db()
    try:
        print("Testing 10-question quiz generation...")
        quiz = await generate_quiz(subject="IPR", num_questions=10)
        print(f"🎉 SUCCESS! Total questions generated: {len(quiz['questions'])}")
        for idx, q in enumerate(quiz['questions']):
            print(f"  [{idx + 1:02d}] {q['question'][:65]}... (Topic: {q.get('topic')})")
    except Exception as e:
        print("❌ Error:", e)
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())

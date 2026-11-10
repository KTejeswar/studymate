import asyncio
from app.database import connect_db, close_db
from app.services.quiz import generate_quiz

async def main():
    await connect_db()
    try:
        print("Testing generate_quiz service...")
        quiz = await generate_quiz(subject="General", num_questions=2)
        print("✅ Quiz generated successfully!")
        print(f"Quiz ID: {quiz['_id']}")
        print(f"Questions generated: {len(quiz['questions'])}")
        for q in quiz['questions']:
            print(f"  • Q{q['id']}: {q['question']}")
    except Exception as e:
        print("❌ Error generating quiz:", e)
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())

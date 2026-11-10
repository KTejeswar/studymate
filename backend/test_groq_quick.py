import asyncio
from app.llm import call_llm

async def main():
    print("Testing Groq API connection...")
    try:
        reply = await call_llm(
            "Explain in 1 simple sentence what Newton's First Law is.",
            system="You are StudyMate, a helpful physics tutor."
        )
        print("\n✅ GROQ IS WORKING!")
        print(f"🤖 Response:\n{reply}\n")
    except Exception as e:
        print("\n❌ Error connecting to Groq:", e)

if __name__ == "__main__":
    asyncio.run(main())

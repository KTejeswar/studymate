import asyncio
from google import genai
from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key.strip('"\''))

async def main():
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say hello in two words!",
        )
        print("✅ SUCCESS! Gemini responded:", response.text)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    asyncio.run(main())

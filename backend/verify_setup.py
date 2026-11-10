import asyncio
from app.llm import get_llm, get_embeddings, call_llm, call_embeddings
from app.config import settings


async def main():
    print("=" * 50)
    print("StudyMate AI System Check")
    print("=" * 50)

    # 1. Config Check
    print("1. Checking API Key Configuration...")
    if settings.gemini_api_key:
        provider = "Google Gemini"
        key_preview = settings.gemini_api_key[:12] + "..." + settings.gemini_api_key[-6:]
    elif settings.openai_api_key:
        provider = "OpenAI"
        key_preview = settings.openai_api_key[:12] + "..." + settings.openai_api_key[-6:]
    elif settings.groq_api_key:
        provider = "Groq"
        key_preview = settings.groq_api_key[:12] + "..." + settings.groq_api_key[-6:]
    else:
        print("❌ No API key found in .env")
        return

    print(f"   Active Provider: {provider}")
    print(f"   Key preview: {key_preview}")

    # 2. LLM Model Check
    print("\n2. Testing Chat Model...")
    try:
        response = await call_llm("Reply with exact words: StudyMate is ready!")
        print(f"   ✅ Chat response: '{response.strip()}'")
    except Exception as e:
        print(f"   ❌ Chat test failed: {e}")
        return

    # 3. Embedding Model Check
    print("\n3. Testing Embedding Model...")
    try:
        embeddings = await call_embeddings(["StudyMate test chunk"])
        vector = embeddings[0]
        print(f"   ✅ Embedding generated successfully!")
        print(f"   Vector length: {len(vector)} dimensions")
    except Exception as e:
        print(f"   ❌ Embedding test failed: {e}")
        return

    print("\n" + "=" * 50)
    print(f"🎉 ALL CHECKS PASSED! Your {provider} setup is 100% working!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())


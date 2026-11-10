import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="sk-b35f9af1956a42a8a13397347aa20644",
    base_url="https://api.deepseek.com",
)

async def main():
    print("Testing DeepSeek connection...")
    try:
        resp = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Say hello in one word!"}],
        )
        print("✅ SUCCESS! DeepSeek answered:", resp.choices[0].message.content)
    except Exception as e:
        print("❌ DeepSeek error:", e)

if __name__ == "__main__":
    asyncio.run(main())

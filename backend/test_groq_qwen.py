from groq import Groq
from dotenv import dotenv_values

env = dotenv_values(".env")
groq_key = env.get("GROQ_API_KEY", "").strip('"\'')

client = Groq(api_key=groq_key)

try:
    print("Testing Groq with model 'qwen/qwen3.8-27b'...")
    res = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": "Explain Newton's first law in 1 short sentence."}],
        max_tokens=50,
    )
    print("\n🎉 SUCCESS! GROQ ANSWERED:")
    print(res.choices[0].message.content)
except Exception as e:
    print("\n❌ Error:", e)

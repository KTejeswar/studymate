import os
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.groq_api_key.strip('"\''))
models = client.models.list()
print("Available Groq models for your key:")
for m in models.data:
    if "llama" in m.id or "mixtral" in m.id or "gemma" in m.id:
        print(f"  • {m.id}")

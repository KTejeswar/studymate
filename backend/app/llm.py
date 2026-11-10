"""
LangChain model configuration and instantiation.
Supports Groq (primary LLM), OpenAI, and LocalFastEmbed for offline zero-cost embeddings.
"""

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from app.config import settings

# ── Model Constants ───────────────────────────────────────────
GROQ_LLM_MODEL = "qwen/qwen3.8-27b"
OPENAI_LLM_MODEL = "gpt-4o-mini"
OPENAI_EMBED_MODEL = "text-embedding-3-small"

_llm: BaseChatModel | None = None
_embeddings: Embeddings | None = None


def get_llm(temperature: float = 0.2) -> BaseChatModel:
    """
    Returns an initialized LangChain ChatModel.
    Checks Groq -> OpenAI in order.
    """
    global _llm
    if _llm is not None:
        return _llm

    if settings.groq_api_key:
        from langchain_groq import ChatGroq
        _llm = ChatGroq(
            model=GROQ_LLM_MODEL,
            groq_api_key=settings.groq_api_key.strip('"\''),
            temperature=temperature,
            max_tokens=900,
        )
    elif settings.openai_api_key:
        from langchain_openai import ChatOpenAI
        _llm = ChatOpenAI(
            model=OPENAI_LLM_MODEL,
            openai_api_key=settings.openai_api_key.strip('"\''),
            temperature=temperature,
            max_tokens=4096,
        )
    else:
        raise ValueError("No valid AI API key found in .env (GROQ_API_KEY or OPENAI_API_KEY).")

    return _llm


class LocalFastEmbed(Embeddings):
    """
    100% Free, local CPU embeddings via fastembed (BAAI/bge-small-en-v1.5).
    Zero API keys needed, zero rate limits, cannot be suspended.
    """
    def __init__(self):
        from fastembed import TextEmbedding
        self._model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [vec.tolist() for vec in self._model.embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        return next(self._model.embed([text])).tolist()

    async def aembed_documents(self, texts: list[str]) -> list[list[float]]:
        import asyncio
        return await asyncio.to_thread(self.embed_documents, texts)

    async def aembed_query(self, text: str) -> list[float]:
        import asyncio
        return await asyncio.to_thread(self.embed_query, text)


def get_embeddings() -> Embeddings:
    """
    Returns an initialized Embeddings model.
    Uses OpenAI if key is present, otherwise falls back to local fastembed.
    """
    global _embeddings
    if _embeddings is not None:
        return _embeddings

    if settings.openai_api_key:
        from langchain_openai import OpenAIEmbeddings
        _embeddings = OpenAIEmbeddings(
            model=OPENAI_EMBED_MODEL,
            openai_api_key=settings.openai_api_key.strip('"\''),
        )
    else:
        _embeddings = LocalFastEmbed()

    return _embeddings


async def call_llm(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Convenience helper to invoke the active ChatModel."""
    llm = get_llm()
    messages = [
        SystemMessage(content=system),
        HumanMessage(content=prompt),
    ]
    response = await llm.ainvoke(messages)
    return response.content if isinstance(response.content, str) else str(response.content)


async def call_embeddings(texts: list[str]) -> list[list[float]]:
    """Convenience helper to generate embeddings for documents."""
    embedder = get_embeddings()
    return await embedder.aembed_documents(texts)


async def call_embedding_query(text: str) -> list[float]:
    """Convenience helper to generate embeddings for a search query."""
    embedder = get_embeddings()
    return await embedder.aembed_query(text)

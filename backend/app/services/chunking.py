"""
Text chunking service.
Splits text per page into ~500 token chunks with 50-token overlap,
preserving metadata (note_id, filename, page, subject).
"""

from typing import Any
import tiktoken

# Use cl100k_base tokenizer (standard for OpenAI & widely used for token estimation)
_encoder = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Return the number of tokens in a text string."""
    return len(_encoder.encode(text))


def split_text_into_chunks(
    text: str,
    chunk_size_tokens: int = 500,
    overlap_tokens: int = 50,
) -> list[str]:
    """
    Split a string into chunks of ~chunk_size_tokens with overlap_tokens overlap.
    Splits by paragraph or sentence boundaries where possible.
    """
    tokens = _encoder.encode(text)
    if not tokens:
        return []

    chunks: list[str] = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size_tokens
        chunk_token_slice = tokens[start:end]
        chunk_str = _encoder.decode(chunk_token_slice).strip()
        if chunk_str:
            chunks.append(chunk_str)

        # Move forward by (chunk_size - overlap)
        start += chunk_size_tokens - overlap_tokens

    return chunks


def prepare_chunks(
    pages: list[str],
    note_id: str,
    filename: str,
    subject: str,
    user_id: str,
    chunk_size_tokens: int = 500,
    overlap_tokens: int = 50,
) -> list[dict[str, Any]]:
    """
    Given a list of page texts (1-indexed page numbering),
    returns a list of chunk dictionaries ready for embedding and MongoDB storage.
    """
    chunk_docs: list[dict[str, Any]] = []

    for page_idx, page_text in enumerate(pages):
        page_num = page_idx + 1
        page_text_clean = page_text.strip()
        if not page_text_clean:
            continue

        raw_chunks = split_text_into_chunks(
            page_text_clean,
            chunk_size_tokens=chunk_size_tokens,
            overlap_tokens=overlap_tokens,
        )

        for chunk_text in raw_chunks:
            chunk_docs.append({
                "note_id": note_id,
                "filename": filename,
                "subject": subject,
                "user_id": user_id,
                "page": page_num,
                "text": chunk_text,
                "token_count": count_tokens(chunk_text),
            })

    return chunk_docs

"""
Tests for token counting and text chunking logic.
"""

from app.services.chunking import (
    count_tokens,
    split_text_into_chunks,
    prepare_chunks,
)


def test_count_tokens():
    text = "Hello world, this is a test for token counting."
    tokens = count_tokens(text)
    assert tokens > 0
    assert isinstance(tokens, int)


def test_split_text_into_chunks_small_text():
    # Text shorter than chunk_size should produce exactly 1 chunk
    text = "Short sentence about artificial intelligence in education."
    chunks = split_text_into_chunks(text, chunk_size_tokens=100, overlap_tokens=10)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_split_text_into_chunks_with_overlap():
    # Long repeated text to ensure multiple chunks are created
    text = ("Machine learning is fascinating. " * 50).strip()
    chunk_size = 50
    overlap = 10
    chunks = split_text_into_chunks(text, chunk_size_tokens=chunk_size, overlap_tokens=overlap)

    assert len(chunks) > 1
    # Check that chunks are non-empty
    for c in chunks:
        assert len(c) > 0


def test_prepare_chunks_page_numbering():
    pages = [
        "Page 1: Introduction to Physics and kinematics.",
        "Page 2: Newton's First Law and inertia.",
        "Page 3: Newton's Second Law and acceleration.",
    ]
    chunks = prepare_chunks(
        pages=pages,
        note_id="test_note_123",
        filename="physics.pdf",
        subject="Physics",
        user_id="demo",
        chunk_size_tokens=100,
        overlap_tokens=10,
    )

    assert len(chunks) == 3
    assert chunks[0]["page"] == 1
    assert chunks[0]["filename"] == "physics.pdf"
    assert chunks[1]["page"] == 2
    assert chunks[2]["page"] == 3
    assert "Newton's First Law" in chunks[1]["text"]

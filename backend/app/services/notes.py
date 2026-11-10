"""
Notes service – upload (extract text), list, and delete notes.
Text extraction: pypdf for PDFs, plain read for TXT/MD.
"""

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
import io

from app.config import settings
from app.database import get_db
from app.llm import call_embeddings
from app.services.chunking import prepare_chunks


ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "text/plain": "txt",
    "text/markdown": "md",
    # Some systems report .md as octet-stream or text/plain
    "application/octet-stream": None,  # we'll check extension
}

ALLOWED_EXTENSIONS = {"pdf", "txt", "md"}


def _get_file_type(filename: str, content_type: str | None) -> str:
    """Determine file type from extension and MIME type."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in ALLOWED_EXTENSIONS:
        return ext

    if content_type and content_type in ALLOWED_TYPES:
        ft = ALLOWED_TYPES[content_type]
        if ft:
            return ft

    raise HTTPException(
        status_code=400,
        detail=f"Unsupported file type: '{ext}'. Allowed: PDF, TXT, MD.",
    )


def _extract_text_pdf(file_bytes: bytes) -> tuple[list[str], int]:
    """Extract text page-by-page from a PDF. Returns (pages_list, page_count)."""
    reader = PdfReader(io.BytesIO(file_bytes))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text.strip())
    return pages, len(pages)


def _extract_text_plain(file_bytes: bytes) -> tuple[list[str], int]:
    """Read TXT/MD as a single 'page'. Returns (pages_list, 1)."""
    text = file_bytes.decode("utf-8", errors="replace").strip()
    return [text], 1


async def upload_note(
    file: UploadFile,
    subject: str = "General",
    user_id: str | None = None,
) -> dict:
    """
    Upload a file, extract its text, and store in the 'notes' collection.
    Returns the inserted document as a dict.
    """
    user_id = user_id or settings.default_user_id

    # ── Validate ────────────────────────────────────────────
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    file_type = _get_file_type(file.filename, file.content_type)

    file_bytes = await file.read()
    if len(file_bytes) > settings.upload_max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.upload_max_size_mb} MB.",
        )

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="File is empty.")

    # ── Extract text ────────────────────────────────────────
    if file_type == "pdf":
        pages, page_count = _extract_text_pdf(file_bytes)
    else:
        pages, page_count = _extract_text_plain(file_bytes)

    full_text = "\n\n".join(pages)
    if not full_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract any text from this file.",
        )

    # ── Store in MongoDB ────────────────────────────────────
    # ── Normalize Subject ───────────────────────────────────
    raw_sub = subject.strip() or "General"
    clean_sub = raw_sub.upper() if len(raw_sub) <= 4 else raw_sub.capitalize()

    doc = {
        "user_id": user_id,
        "filename": file.filename,
        "file_type": file_type,
        "subject": clean_sub,
        "pages": pages,           # list of strings, one per page
        "page_count": page_count,
        "created_at": datetime.now(timezone.utc),
    }

    db = get_db()
    result = await db.notes.insert_one(doc)
    doc["_id"] = result.inserted_id
    note_id_str = str(result.inserted_id)

    # ── Chunk & Embed ───────────────────────────────────────
    chunk_docs = prepare_chunks(
        pages=pages,
        note_id=note_id_str,
        filename=file.filename,
        subject=doc["subject"],
        user_id=user_id,
    )

    if chunk_docs:
        # Generate embeddings in batch
        texts_to_embed = [c["text"] for c in chunk_docs]
        print(f"🔄 Generating embeddings for {len(chunk_docs)} chunks ({file.filename})...")
        embeddings = await call_embeddings(texts_to_embed)

        for chunk_doc, emb in zip(chunk_docs, embeddings):
            chunk_doc["embedding"] = emb

        await db.chunks.insert_many(chunk_docs)
        print(f"✅ Successfully stored {len(chunk_docs)} embedded chunks in MongoDB for '{file.filename}'")

    return doc


async def list_notes(user_id: str | None = None) -> list[dict]:
    """Return all notes for the given user, newest first."""
    user_id = user_id or settings.default_user_id
    db = get_db()
    cursor = db.notes.find(
        {"user_id": user_id},
        {"pages": 0},  # don't return full text in the list
    ).sort("created_at", -1)
    return await cursor.to_list(length=200)


async def delete_note(note_id: str, user_id: str | None = None) -> bool:
    """Delete a note and its chunks. Returns True if found."""
    user_id = user_id or settings.default_user_id
    db = get_db()

    try:
        oid = ObjectId(note_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid note ID format.")

    result = await db.notes.delete_one({"_id": oid, "user_id": user_id})
    # Also delete associated chunks (will exist after Step 5)
    await db.chunks.delete_many({"note_id": note_id, "user_id": user_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found.")
    return True

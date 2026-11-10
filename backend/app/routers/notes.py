"""
Notes router – upload, list, and delete notes.
"""

from fastapi import APIRouter, UploadFile, File, Form

from app.models.notes import NoteOut, NoteUploadOut, NoteListOut, NoteDeleteOut
from app.services.notes import upload_note, list_notes, delete_note

router = APIRouter(prefix="/api/notes", tags=["notes"])


def _doc_to_note_out(doc: dict) -> NoteOut:
    """Convert a MongoDB document to a NoteOut response."""
    return NoteOut(
        id=str(doc["_id"]),
        user_id=doc["user_id"],
        filename=doc["filename"],
        file_type=doc["file_type"],
        subject=doc["subject"],
        page_count=doc["page_count"],
        created_at=doc["created_at"],
    )


@router.post("", response_model=NoteUploadOut, status_code=201)
async def upload(
    file: UploadFile = File(..., description="PDF, TXT, or MD file"),
    subject: str = Form("General", description="Subject / course name"),
):
    """Upload a note file. Text is extracted and stored."""
    doc = await upload_note(file, subject)
    return NoteUploadOut(note=_doc_to_note_out(doc))


@router.get("", response_model=NoteListOut)
async def list_all():
    """List all uploaded notes (newest first)."""
    docs = await list_notes()
    notes = [_doc_to_note_out(d) for d in docs]
    return NoteListOut(notes=notes, count=len(notes))


@router.delete("/{note_id}", response_model=NoteDeleteOut)
async def delete(note_id: str):
    """Delete a note and its chunks."""
    await delete_note(note_id)
    return NoteDeleteOut(id=note_id)

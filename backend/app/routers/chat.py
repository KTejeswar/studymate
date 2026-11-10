"""
Chat API router – invokes the LangGraph StudyMate agent.
"""

from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse, CitationOut
from app.agent.graph import study_agent
from app.config import settings

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Send a question to the StudyMate LangGraph agent.
    Returns the answer, citations (file + page), and execution steps.
    """
    try:
        initial_state = {
            "question": req.question,
            "subject": req.subject,
            "user_id": settings.default_user_id,
            "needs_retrieval": True,
            "chunks": [],
            "is_relevant": False,
            "rewrite_count": 0,
            "answer": "",
            "citations": [],
            "steps_log": [],
        }

        # Run the LangGraph agent
        final_state = await study_agent.ainvoke(initial_state)

        citations_out = [
            CitationOut(
                filename=c.get("filename", ""),
                page=c.get("page", 1),
                subject=c.get("subject", "General"),
                snippet=c.get("snippet", ""),
            )
            for c in final_state.get("citations", [])
        ]

        return ChatResponse(
            answer=final_state.get("answer", "I could not find this in your notes."),
            citations=citations_out,
            steps=final_state.get("steps_log", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

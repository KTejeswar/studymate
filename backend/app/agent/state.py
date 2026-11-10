"""
State definition for the StudyMate LangGraph agent.
"""

from typing import TypedDict, Any


class AgentState(TypedDict):
    question: str
    subject: str | None
    user_id: str
    needs_retrieval: bool
    chunks: list[dict[str, Any]]
    is_relevant: bool
    rewrite_count: int
    answer: str
    citations: list[dict[str, Any]]
    steps_log: list[str]

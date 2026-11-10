"""
LangGraph compilation for StudyMate RAG Agent.
Includes conditional routing, cycle guardrails (max 2 rewrites), and step logging.
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState
from app.agent.nodes import (
    decide_node,
    retrieve_node,
    grade_chunks_node,
    rewrite_query_node,
    generate_answer_node,
)


def decide_routing(state: AgentState) -> Literal["retrieve", "end"]:
    """Branch after decide node: retrieve or finish immediately."""
    if state.get("needs_retrieval", True):
        return "retrieve"
    return "end"


def grade_routing(state: AgentState) -> Literal["generate_answer", "rewrite_query"]:
    """
    Branch after grade_chunks:
    If relevant -> generate answer.
    If not relevant and rewrite_count < 2 -> rewrite query and try again.
    Else -> generate answer (which will return 'not found').
    """
    if state.get("is_relevant", False):
        return "generate_answer"

    if state.get("rewrite_count", 0) < 2:
        return "rewrite_query"

    return "generate_answer"


def build_agent():
    """Build and compile the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # 1. Add nodes
    workflow.add_node("decide", decide_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade_chunks", grade_chunks_node)
    workflow.add_node("rewrite_query", rewrite_query_node)
    workflow.add_node("generate_answer", generate_answer_node)

    # 2. Add edges & conditional branching
    workflow.add_edge(START, "decide")

    workflow.add_conditional_edges(
        "decide",
        decide_routing,
        {
            "retrieve": "retrieve",
            "end": END,
        },
    )

    workflow.add_edge("retrieve", "grade_chunks")

    workflow.add_conditional_edges(
        "grade_chunks",
        grade_routing,
        {
            "generate_answer": "generate_answer",
            "rewrite_query": "rewrite_query",
        },
    )

    # Loop back from rewrite to retrieve
    workflow.add_edge("rewrite_query", "retrieve")

    # Final edge to finish
    workflow.add_edge("generate_answer", END)

    return workflow.compile()


# Singleton compiled graph instance
study_agent = build_agent()

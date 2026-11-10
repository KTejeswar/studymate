"""
Quiz router – endpoints to generate quizzes and submit answers.
"""

from fastapi import APIRouter
from app.models.quiz import (
    QuizGenerateRequest,
    QuizOut,
    QuizQuestionOut,
    QuestionOption,
    QuizSubmitRequest,
    QuizSubmitResult,
    QuestionResult,
)
from app.services.quiz import generate_quiz, submit_quiz
from app.config import settings

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.post("", response_model=QuizOut, status_code=201)
async def create_quiz(req: QuizGenerateRequest):
    """
    Generate multiple-choice questions from notes.
    Hides correct answers from the response.
    """
    quiz_doc = await generate_quiz(
        subject=req.subject,
        topic=req.topic,
        num_questions=req.num_questions,
        user_id=settings.default_user_id,
    )

    # Sanitize questions (hide correct_option & explanation until submission)
    client_questions = []
    for q in quiz_doc["questions"]:
        opts = [QuestionOption(id=o["id"], text=o["text"]) for o in q.get("options", [])]
        client_questions.append(
            QuizQuestionOut(
                id=q["id"],
                question=q["question"],
                options=opts,
                topic=q.get("topic", "General"),
                citation=q.get("citation"),
            )
        )

    return QuizOut(
        id=str(quiz_doc["_id"]),
        subject=quiz_doc["subject"],
        topic=quiz_doc.get("topic"),
        num_questions=quiz_doc["num_questions"],
        questions=client_questions,
        created_at=quiz_doc["created_at"],
    )


@router.post("/{quiz_id}/submit", response_model=QuizSubmitResult)
async def submit_answers(quiz_id: str, req: QuizSubmitRequest):
    """
    Submit answers for a quiz. Grades the questions, updates topic stats,
    and returns score, explanations, and review details.
    """
    attempt = await submit_quiz(
        quiz_id=quiz_id,
        submitted_answers=[a.model_dump() for a in req.answers],
        user_id=settings.default_user_id,
    )

    results = [QuestionResult(**r) for r in attempt["results"]]

    return QuizSubmitResult(
        attempt_id=str(attempt["_id"]),
        quiz_id=attempt["quiz_id"],
        total_questions=attempt["total_questions"],
        correct_count=attempt["correct_count"],
        wrong_count=attempt["wrong_count"],
        score_percentage=attempt["score_percentage"],
        results=results,
        submitted_at=attempt["submitted_at"],
    )

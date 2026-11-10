"""
Quiz generation and grading service.
Generates MCQs strictly from note chunks and records attempts.
"""

import json
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import HTTPException

from app.config import settings
from app.database import get_db
from app.llm import call_llm


QUIZ_SYSTEM_PROMPT = """You are an expert academic examiner.
Generate multiple-choice questions based ONLY on the provided notes excerpts.

Keep explanations concise (1 short sentence) so responses complete cleanly.

STRICT JSON OUTPUT FORMAT:
You must respond with ONLY valid JSON (no markdown wrappers, no extra text):
{
  "questions": [
    {
      "id": 1,
      "question": "What is ...?",
      "options": [
        {"id": "A", "text": "First option"},
        {"id": "B", "text": "Second option"},
        {"id": "C", "text": "Third option"},
        {"id": "D", "text": "Fourth option"}
      ],
      "correct_option": "A",
      "explanation": "Brief 1-sentence explanation why A is correct.",
      "topic": "Concise 1-3 word topic tag",
      "citation": "filename.pdf, Page X"
    }
  ]
}
"""


async def generate_quiz(
    subject: str = "General",
    topic: str | None = None,
    num_questions: int = 3,
    user_id: str = "demo",
) -> dict:
    """
    Fetch relevant note chunks and prompt the LLM to generate MCQs.
    """
    db = get_db()

    # 1. Fetch chunks for the subject (or any chunk if General)
    query: dict = {"user_id": user_id}
    sub_lower = subject.lower().strip() if subject else "general"
    if sub_lower not in ("general", "all", "all subjects (general)", ""):
        query["subject"] = {"$regex": f"^{subject.strip()}$", "$options": "i"}

    cursor = db.chunks.find(query).limit(15)
    chunks = await cursor.to_list(length=15)

    if not chunks:
        # Fallback to any chunk
        chunks = await db.chunks.find({"user_id": user_id}).limit(10).to_list(length=10)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No uploaded notes found. Please upload notes before generating a quiz.",
        )

    # 2. Build context
    context_parts = []
    for c in chunks[:8]:
        context_parts.append(f"[File: {c.get('filename')}, Page: {c.get('page')}]\n{c.get('text')}")
    context = "\n\n---\n\n".join(context_parts)

    prompt = (
        f"Generate {num_questions} high-quality multiple choice question(s) from these notes.\n"
        f"Subject: {subject}\n"
    )
    if topic:
        prompt += f"Focus specifically on the topic: '{topic}'\n"

    prompt += f"\n=== NOTES EXCERPTS ===\n{context}\n======================="

    raw_response = await call_llm(prompt, system=QUIZ_SYSTEM_PROMPT)

    # 3. Parse JSON safely with repair fallback
    questions = []
    clean = raw_response.strip().removeprefix("```json").removesuffix("```").strip()

    try:
        data = json.loads(clean)
        questions = data.get("questions", [])
    except Exception:
        # Auto-repair truncated JSON: find the last complete question object
        import re
        try:
            # If the closing array/object bracket was cut off, close it
            last_brace = clean.rfind("}")
            if last_brace != -1:
                repaired = clean[:last_brace + 1] + "\n]}"
                data = json.loads(repaired)
                questions = data.get("questions", [])
        except Exception:
            pass

        # Final regex fallback to extract any completed question dicts
        if not questions:
            matches = re.findall(r'\{\s*"id"\s*:\s*\d+.*?"topic"\s*:\s*"[^"]*".*?\}', clean, re.DOTALL)
            for m in matches:
                try:
                    q_obj = json.loads(m)
                    questions.append(q_obj)
                except Exception:
                    continue

    if not questions:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate structured quiz. Please try generating with fewer questions (e.g. 5).",
        )

    # 4. Save quiz to MongoDB
    quiz_doc = {
        "user_id": user_id,
        "subject": subject,
        "topic": topic,
        "num_questions": len(questions),
        "questions": questions,  # contains correct_option + explanation
        "created_at": datetime.now(timezone.utc),
    }

    result = await db.quizzes.insert_one(quiz_doc)
    quiz_doc["_id"] = result.inserted_id
    return quiz_doc


async def submit_quiz(
    quiz_id: str,
    submitted_answers: list[dict],
    user_id: str = "demo",
) -> dict:
    """
    Grades user answers against stored quiz questions,
    records topic wins/losses, and stores the attempt.
    """
    db = get_db()

    try:
        oid = ObjectId(quiz_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid quiz ID.")

    quiz = await db.quizzes.find_one({"_id": oid, "user_id": user_id})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found.")

    questions = quiz.get("questions", [])
    answers_map = {a["question_id"]: a["selected_option"].upper().strip() for a in submitted_answers}

    results = []
    correct_count = 0
    topic_results = []  # for updating topic stats in Step 12

    for q in questions:
        qid = q.get("id")
        correct_opt = q.get("correct_option", "A").upper().strip()
        user_choice = answers_map.get(qid, "")
        is_correct = (user_choice == correct_opt)

        if is_correct:
            correct_count += 1

        topic_tag = q.get("topic", "General")
        topic_results.append({
            "topic": topic_tag,
            "subject": quiz.get("subject", "General"),
            "is_correct": is_correct,
        })

        results.append({
            "question_id": qid,
            "question": q.get("question", ""),
            "selected_option": user_choice,
            "correct_option": correct_opt,
            "is_correct": is_correct,
            "explanation": q.get("explanation", ""),
            "topic": topic_tag,
        })

    total = len(questions)
    wrong_count = total - correct_count
    score_percentage = round((correct_count / total) * 100, 1) if total > 0 else 0.0

    # 5. Save attempt
    attempt_doc = {
        "user_id": user_id,
        "quiz_id": quiz_id,
        "subject": quiz.get("subject", "General"),
        "total_questions": total,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
        "score_percentage": score_percentage,
        "topic_results": topic_results,
        "results": results,
        "submitted_at": datetime.now(timezone.utc),
    }

    insert_res = await db.attempts.insert_one(attempt_doc)
    attempt_doc["_id"] = insert_res.inserted_id

    # 6. Update topic_stats collection (aggregated counts)
    for tr in topic_results:
        await db.topic_stats.update_one(
            {"user_id": user_id, "topic": tr["topic"]},
            {
                "$inc": {
                    "total_attempts": 1,
                    "correct": 1 if tr["is_correct"] else 0,
                    "wrong": 0 if tr["is_correct"] else 1,
                },
                "$set": {
                    "subject": tr["subject"],
                    "updated_at": datetime.now(timezone.utc),
                },
            },
            upsert=True,
        )

    return attempt_doc

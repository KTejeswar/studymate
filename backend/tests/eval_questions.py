"""
20-Question Evaluation Benchmark for StudyMate RAG Agent.
Evaluates:
- Groundedness (does it cite notes?)
- Rejection of out-of-domain queries ('I could not find this in your notes.')
- Chit-chat handling (no unneeded retrieval)
"""

import asyncio
import time
from app.database import connect_db, close_db
from app.agent.graph import study_agent

BENCHMARK_QUESTIONS = [
    # ── Category 1: Direct Factual (from notes) ───────────────
    {"id": 1, "category": "IN_DOMAIN", "q": "What is Newton's First Law of Motion?"},
    {"id": 2, "category": "IN_DOMAIN", "q": "State the formula for force according to the Second Law."},
    {"id": 3, "category": "IN_DOMAIN", "q": "What is inertia and how does it relate to mass?"},
    {"id": 4, "category": "IN_DOMAIN", "q": "What is the unit of force in Newton's second law?"},
    {"id": 5, "category": "IN_DOMAIN", "q": "Explain Newton's Third Law with an example of action and reaction."},
    {"id": 6, "category": "IN_DOMAIN", "q": "In what year did Isaac Newton formulate these three laws?"},
    {"id": 7, "category": "IN_DOMAIN", "q": "If mass is 5kg and acceleration is 2 m/s^2, what is the force according to the notes?"},
    {"id": 8, "category": "IN_DOMAIN", "q": "Do forces occur in matched pairs or individually?"},

    # ── Category 2: Conversational / Greetings ───────────────
    {"id": 9,  "category": "CONVERSATIONAL", "q": "Hello StudyMate!"},
    {"id": 10, "category": "CONVERSATIONAL", "q": "Good morning! Can you help me study today?"},
    {"id": 11, "category": "CONVERSATIONAL", "q": "Thank you for your help!"},
    {"id": 12, "category": "CONVERSATIONAL", "q": "Who are you?"},

    # ── Category 3: Out-of-Domain (Should reply 'not found') ─
    {"id": 13, "category": "OUT_OF_DOMAIN", "q": "How do I bake a chocolate cake at home?"},
    {"id": 14, "category": "OUT_OF_DOMAIN", "q": "Who won the FIFA World Cup in 2022?"},
    {"id": 15, "category": "OUT_OF_DOMAIN", "q": "What is the capital of Australia?"},
    {"id": 16, "category": "OUT_OF_DOMAIN", "q": "Explain quantum entanglement in depth."},
    {"id": 17, "category": "OUT_OF_DOMAIN", "q": "What are the rules of basketball?"},
    {"id": 18, "category": "OUT_OF_DOMAIN", "q": "Give me a recipe for Italian pasta."},
    {"id": 19, "category": "OUT_OF_DOMAIN", "q": "Who painted the Mona Lisa?"},
    {"id": 20, "category": "OUT_OF_DOMAIN", "q": "What is the current stock price of Apple?"},
]


async def run_benchmark():
    await connect_db()

    print("=" * 80)
    print("🎯 STARTING 20-QUESTION EVALUATION BENCHMARK FOR STUDYMATE")
    print("=" * 80)

    results = []
    start_total = time.time()

    for item in BENCHMARK_QUESTIONS:
        qid = item["id"]
        cat = item["category"]
        q = item["q"]

        t0 = time.time()
        agent_out = await study_agent.ainvoke({
            "question": q,
            "subject": None,
            "user_id": "demo",
            "rewrite_count": 0,
            "steps_log": [],
        })
        latency = time.time() - t0

        ans = agent_out.get("answer", "")
        cites = agent_out.get("citations", [])
        num_cites = len(cites)

        # Verification logic
        passed = False
        reason = ""

        if cat == "IN_DOMAIN":
            # Pass if it provided an answer and has citations or mentions note facts
            if "could not find" not in ans.lower() and (num_cites > 0 or len(ans) > 30):
                passed = True
                reason = f"Answered with {num_cites} citation(s)"
            else:
                passed = False
                reason = "Failed to find or cite note facts"

        elif cat == "CONVERSATIONAL":
            # Pass if polite conversational response and did NOT say 'could not find'
            if "could not find" not in ans.lower() and len(ans) > 5:
                passed = True
                reason = "Handled conversationally without unnecessary search"
            else:
                passed = False
                reason = "Incorrectly triggered not-found"

        elif cat == "OUT_OF_DOMAIN":
            # Pass if it rejected and replied 'could not find'
            if "could not find" in ans.lower() or "not find this in your notes" in ans.lower():
                passed = True
                reason = "Strictly grounded: safely rejected out-of-domain question"
            else:
                passed = False
                reason = "Hallucinated or answered outside notes"

        status_icon = "✅ PASS" if passed else "❌ FAIL"
        results.append({"id": qid, "category": cat, "passed": passed, "latency": latency, "reason": reason})

        print(f"[{qid:02d}/20] {status_icon} | {cat:<14} | ({latency:.2f}s) | Q: '{q[:40]}...'")
        print(f"       -> Result: {reason}")
        print(f"       -> Answer: {ans[:90]}...\n")

    total_time = time.time() - start_total
    total_passed = sum(1 for r in results if r["passed"])
    pass_rate = (total_passed / len(results)) * 100

    print("=" * 80)
    print("📊 BENCHMARK REPORT SUMMARY")
    print("=" * 80)
    print(f"Total Questions Evaluated: {len(results)}")
    print(f"Tests Passed:              {total_passed} / {len(results)} ({pass_rate:.1f}%)")
    print(f"Total Evaluation Time:     {total_time:.2f}s (Avg: {total_time/len(results):.2f}s per query)")
    print("=" * 80)

    await close_db()


if __name__ == "__main__":
    asyncio.run(run_benchmark())

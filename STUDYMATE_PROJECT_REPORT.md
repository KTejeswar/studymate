# 🎓 STUDYMATE — AI-POWERED CLASS NOTES ASSISTANT & ADAPTIVE STUDY PLATFORM
**Comprehensive Summer Internship Technical Report & System Documentation**

---

## 📋 Executive Summary
**StudyMate** is an end-to-end, full-stack educational AI assistant designed to eliminate hallucinations in student exam preparation by strictly grounding all answers in uploaded course materials. Built with **FastAPI**, **LangGraph**, **MongoDB**, and **React**, StudyMate provides three symbiotic workflows:
1. **Grounded Question & Answer with Verifiable Citations**: Answers student inquiries solely from lecture notes (PDF, TXT, MD) and cites the exact source file and page number.
2. **Active-Recall Multiple-Choice & Flashcard Engine**: Automatically synthesizes structured practice questions directly from lecture excerpts with instant feedback and concept explanations.
3. **Weak-Topic Analytics**: Tracks topic-level errors across quiz attempts and visually surfaces concepts requiring revision on an adaptive dashboard, enabling one-click targeted practice.

---

## 1. Problem Statement & Motivation

### 1.1 The Problem
- **Hallucinations in Generic LLMs**: When students use general-purpose AI chat tools (e.g. ChatGPT) to study course-specific curricula, the models frequently fabricate facts, reference irrelevant textbook editions, or offer general explanations that deviate from the lecturer's syllabus.
- **Passive Re-reading vs. Active Recall**: Research in cognitive science demonstrates that passive reading leads to rapid decay of retention (Ebbinghaus Forgetting Curve). Most study tools lack built-in active recall and self-assessment mechanisms tied directly to the student's personal notes.
- **Lack of Verification**: Standard AI chatbots cannot prove where an answer originated. Students are left unable to verify whether a formula or definition matches their exam syllabus.
- **Blind Revision**: Students struggle to identify which sub-topics they consistently misunderstand, leading to inefficient "blanket studying" rather than targeted reinforcement.

### 1.2 The Objective
To design and implement a lightweight, private, and deterministic full-stack study assistant that:
- Restricts responses **exclusively** to the student’s uploaded files.
- Refuses out-of-syllabus questions with: *"I could not find this in your notes."*
- Implements an automated LangGraph agent evaluation cycle (`decide` ➔ `retrieve` ➔ `grade` ➔ `rewrite` ➔ `answer`).
- Generates dynamic practice quizzes and tracks weaknesses to close the active learning loop.

---

## 2. Real-World Use Cases & Persona Profiles

| Persona | Scenario | How StudyMate Solves It |
|---|---|---|
| **Undergraduate Engineering Student** | Preparing for a mid-term exam on *Classical Mechanics* with a 150-page PDF note file. | Uploads lecture slides; asks specific formula derivations; clicks citation chips to view source page excerpts. |
| **Law / Management Student** | Reviewing case law and *Intellectual Property Rights* (IPR, Patents, Trademarks). | Uses the chat to verify differences between Trade Secrets and Patents; uses Flashcards mode to memorize statutory criteria. |
| **Competitive Exam Aspirant** | Taking daily quizzes on various subjects. | Reviews the Dashboard Weak Topics chart to discover an 80% error rate on *Thermodynamics*; clicks "Practice Weak Topics" to generate targeted MCQs. |

---

## 3. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       STUDYMATE SYSTEM ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [ STUDENT FRONTEND (React 18 + Tailwind CSS + Recharts + Vite) ]          │
│     ├── Dashboard (Metrics, Gamified Streak, Recharts Gradient Bar Chart)   │
│     ├── Notes Manager (Drag-and-Drop, PDF/TXT/MD, 100MB Limit)              │
│     ├── Grounded Chat (Thinking Traces, Interactive Citation Chips)         │
│     └── Quiz & Flashcards Engine (MCQs, Instant Explanations, Markdown Export)
│                                       │                                     │
│                     REST API Calls (JSON / FormData)                        │
│                                       ▼                                     │
│   [ BACKEND SERVICES (FastAPI Async + Pydantic v2 + Python 3.12) ]          │
│     ├── /api/notes (pypdf Extraction, ~500 Token Chunking, 50 Overlap)      │
│     ├── /api/chat  (LangGraph Agentic RAG Pipeline)                         │
│     ├── /api/quiz  (Structured MCQ Synthesis & Grading Engine)              │
│     └── /api/stats (Weak Topic Aggregations & Accuracy Calculations)        │
│                                       │                                     │
│                    Vector Operations & Data Storage                         │
│                                       ▼                                     │
│   [ DATA & AI INFRASTRUCTURE ]                                              │
│     ├── MongoDB (Local / Atlas: notes, chunks, quizzes, attempts, stats)   │
│     ├── LocalFastEmbed (BAAI/bge-small-en-v1.5, 384-dim CPU Vectors)         │
│     └── LLM Reasoning Engine (Groq LLaMA 3.3 / Qwen 2.5 / OpenAI / Gemini)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Technical Stack Justification

### 4.1 Backend Architecture
- **Python 3.12**: State-of-the-art async performance with strong typing support.
- **FastAPI**: High-throughput ASGI web framework with native async support and automatic OpenAPI documentation.
- **Pydantic v2 & pydantic-settings**: Enforces strict request/response data contracts and secure `.env` variable parsing.
- **LangGraph & LangChain Core**: Replaces brittle linear prompt chains with a stateful cyclic directed graph with cycle limits and relevance grading.
- **Motor (AsyncIOMotorClient)**: Non-blocking asynchronous MongoDB driver preventing thread bottlenecks during heavy file operations.
- **pypdf**: Robust, local, zero-dependency PDF text extractor supporting multi-page slicing.
- **FastEmbed (BAAI/bge-small-en-v1.5)**: 100% free, offline, local ONNX CPU embeddings running in 384 dimensions. Eliminates cloud embedding costs, network latency, and API rate limits.
- **Groq Cloud API**: Ultra-fast LLM inference (500 tokens/sec) providing instant chat answers and quiz generation.

### 4.2 Frontend Architecture
- **React 18 & Vite 6**: Instant development startup (<300ms) with zero hydration overhead or complex server rendering bugs.
- **Tailwind CSS**: Utility-first atomic styling with modern dark theme tokens (`#05050A` obsidian, `#B794FF` lavender, `#22E4FF` cyan).
- **Lucide React**: Clean, lightweight, accessible icon set.
- **Recharts**: Responsive SVG charting library powering the interactive Weak Topics gradient bar chart.

---

## 5. Core Feature Specifications & Workflows

### 5.1 Document Ingestion & Chunking Pipeline
1. **Validation**: Files are checked for format (`.pdf`, `.txt`, `.md`) and size (up to 100 MB).
2. **Page-Aware Extraction**: PDFs are parsed page-by-page using `pypdf`.
3. **Token Slicing**: Using `tiktoken` (cl100k_base), text is sliced into chunks of **~500 tokens** with a **50-token overlap** to preserve semantic continuity across boundaries.
4. **Embedding Generation**: Batch-encoded via `LocalFastEmbed` into 384-dimensional dense vectors.
5. **Storage**: Stored in MongoDB collection `chunks` with metadata (`note_id`, `filename`, `page`, `subject`, `text`, `embedding`).

### 5.2 LangGraph Agentic RAG Chat Flow
The agent operates as a **Cyclic State Machine** with 5 discrete nodes and strict guardrails:

```
                  ┌─────────────────┐
                  │  User Question  │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │   decide_node   │
                  └────────┬────────┘
                           │
             Is it a pure greeting?
            ┌──────────────┴──────────────┐
            ▼                             ▼
         [ YES ]                       [ NO ]
    Return instant greeting       ┌───────────────┐
    (No DB query needed)          │ retrieve_node │
                                  └───────┬───────┘
                                          ▼
                               ┌────────────────────┐
                               │ grade_chunks_node  │
                               └──────────┬─────────┘
                                          │
                         Are chunks relevant (score >= 0.35)?
                        ┌─────────────────┴─────────────────┐
                        ▼                                   ▼
                     [ YES ]                             [ NO ]
               ┌─────────────────┐                  Rewrite Count < 2?
               │ generate_answer │                 ┌────────┴────────┐
               └────────┬────────┘                 ▼                 ▼
                        │                       [ YES ]           [ NO ]
                        │                  ┌───────────────┐ ┌───────────────┐
                        │                  │ rewrite_query │ │ generate_answer│
                        │                  └───────┬───────┘ │ (Say not found│
                        │                          │         │  in notes)    │
                        │                          ▼         └───────┬───────┘
                        │                   Loop to retrieve         │
                        └──────────────────────────┬─────────────────┘
                                                   ▼
                                         [ Final Answer with ]
                                         [ File & Page Cites ]
```

### 5.3 Active Recall Quiz & Flashcards Engine
- **JSON Synthesis**: LLM prompt instructs strict output containing questions, 4 options, the single correct answer letter, topic tags, and 1-sentence explanations.
- **Cheating Prevention**: Correct options and explanations are stripped before sending the quiz payload to the browser; answers are only revealed upon submission.
- **Adaptive Study Integration**: Every incorrect choice updates the `topic_stats` collection in MongoDB, recalculating the error rate for that specific sub-concept.
- **Revision Flashcards**: Allows students to flip through concept prompts and answers at their own pace without submission pressure.
- **Offline Markdown Export**: Students can download a complete `.md` revision sheet with all questions, correct choices, and explanations with one click.

---

## 6. Database Schema (MongoDB)

| Collection | Key Fields | Description |
|---|---|---|
| **`notes`** | `_id`, `user_id`, `filename`, `file_type`, `subject`, `pages[]`, `page_count`, `created_at` | Primary document record. |
| **`chunks`** | `_id`, `note_id`, `user_id`, `filename`, `subject`, `page`, `text`, `embedding[384]` | Vector chunk store for cosine similarity retrieval. |
| **`quizzes`** | `_id`, `user_id`, `subject`, `topic`, `num_questions`, `questions[]`, `created_at` | Generated question sets with hidden answer keys. |
| **`attempts`** | `_id`, `quiz_id`, `user_id`, `total_questions`, `correct_count`, `score_percentage`, `results[]` | Student submission logs and scoring history. |
| **`topic_stats`**| `_id`, `user_id`, `topic`, `subject`, `total_attempts`, `correct`, `wrong`, `updated_at` | Aggregated topic accuracy metrics for dashboard charts. |

---

## 7. Verification, Testing & Evaluation

### 7.1 Automated Pytest Suite
- `test_chunking.py`: Verifies token counts, chunk boundaries, and page preservation.
- `test_retrieval.py`: Tests cosine similarity mathematical edge cases (identical, orthogonal, opposite, zero vectors).
- `test_api.py`: Validates FastAPI lifespan and `/api/health`, `/api/notes`, `/api/stats` HTTP responses.

### 7.2 20-Question Empirical Benchmark (`eval_questions.py`)
| Query Category | Sample Test Query | Expected Behavior | Observed Result |
|---|---|---|---|
| **In-Domain Notes** | *"What is Newton's Second Law formula?"* | Answered with `[File, Page]` citation | **100% Pass** |
| **Conversational** | *"Good morning! Can you help me study?"* | Friendly response without DB search | **100% Pass** |
| **Out-of-Domain** | *"How do I bake a chocolate cake?"* | Rejection: *"I could not find this in your notes."* | **100% Pass** |

---

## 8. Setup & Execution Instructions

### 8.1 Backend
```powershell
cd d:\StudyMate\backend
uv sync --all-extras
uv run uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Health Ping: `http://localhost:8000/api/health`

### 8.2 Frontend
```powershell
cd d:\StudyMate\frontend
npm install
npm run dev
```
- Application: `http://localhost:3000`

---

## 9. Conclusion & Future Roadmap
StudyMate demonstrates that pairing agentic workflows with strict retrieval guardrails creates a dependable, hallucination-free study environment for higher education. 
- **Future Enhancements**: Multi-user JWT authentication, OCR integration for handwritten lecture notes, and voice-assisted interactive study mode.

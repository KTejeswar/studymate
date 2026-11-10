# 🎓 StudyMate — AI Study Assistant

> A modern, full-stack AI study assistant built with FastAPI, LangGraph, MongoDB, and React. Students can upload class notes (PDF/TXT/MD), ask questions with verifiable citations (file + page), take auto-generated practice quizzes, and track their weakest topics through real-time analytics.

---

## 🌟 Key Features

1. **Class Notes Ingestion & RAG Pipeline**
   - Upload PDF, TXT, or Markdown documents.
   - Token-aware chunking (~500 tokens with 50-token overlap) preserving source page numbers.
   - High-performance vector embeddings with cosine similarity retrieval.

2. **Grounded Q&A Agent (LangGraph)**
   - Multi-step evaluation graph: `decide` ➔ `retrieve` ➔ `grade_chunks` ➔ `rewrite_query` (max 2 retries) ➔ `generate_answer`.
   - Strict grounding: answers ONLY using facts from uploaded notes and provides file & page citations.
   - Out-of-domain rejection: safely replies *"I could not find this in your notes"* rather than hallucinating.

3. **Active-Recall Quiz Generator**
   - Generates 4-option multiple-choice questions grounded in note excerpts.
   - Conceals correct answers until submission.
   - Instant scoring with per-question explanations and topic tags.

4. **Weak-Topics Tracker & Analytics**
   - Aggregates accuracy and error rates across all quiz attempts.
   - Interactive bar chart visualizing the student's weakest concepts.
   - One-click **"Practice Weak Topics"** button to auto-generate targeted revision quizzes.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12, FastAPI, Uvicorn, LangGraph, Motor (Async MongoDB), PyPDF, FastEmbed / Groq / OpenAI.
- **Database:** Local MongoDB (`studymate` database with `notes`, `chunks`, `quizzes`, `attempts`, `topic_stats`).
- **Frontend:** React, Vite, Tailwind CSS, Recharts, Lucide React Icons.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.12+
- Node.js 18+
- Local MongoDB running on `mongodb://localhost:27017`

---

### 2. Backend Setup

```powershell
cd d:\StudyMate\backend

# Install dependencies
uv sync --all-extras

# Start the FastAPI backend
uv run uvicorn app.main:app --reload --port 8000
```
- Interactive API Docs (Swagger UI): **`http://localhost:8000/docs`**
- Health Check: **`http://localhost:8000/api/health`**

---

### 3. Frontend Setup

```powershell
cd d:\StudyMate\frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
- App UI: **`http://localhost:3000`**

---

## 🧪 Testing & Evaluation

### Run Pytest Suite
```powershell
cd d:\StudyMate\backend
uv run pytest tests/ -v
```
Tests token chunking, cosine similarity math, and full API integration endpoints.

### Run 20-Question Evaluation Benchmark
```powershell
cd d:\StudyMate\backend
python tests/eval_questions.py
```
Runs a 20-question test evaluating in-domain grounding, conversational greetings, and out-of-domain rejections.

---

## 📁 Project Architecture

```
d:\StudyMate\
├── backend/
│   ├── app/
│   │   ├── agent/            # LangGraph agent (state, nodes, graph, tools)
│   │   ├── models/           # Pydantic schemas (notes, chat, quiz, stats)
│   │   ├── routers/          # FastAPI routers (notes, chat, quiz, stats, health)
│   │   ├── services/         # Business logic (chunking, retrieval, quiz, stats)
│   │   ├── config.py         # App configuration
│   │   ├── database.py       # Motor async MongoDB singleton
│   │   ├── llm.py            # AI model wrappers (Groq/OpenAI/FastEmbed)
│   │   └── main.py           # FastAPI entrypoint & CORS
│   └── tests/                # Pytest suite & 20-question benchmark
│
├── frontend/
│   ├── src/
│   │   ├── components/       # Sidebar, Dashboard, Notes, Chat, Quiz
│   │   ├── lib/              # Centralized API client (api.js)
│   │   ├── App.jsx           # Single-page application router
│   │   └── main.jsx          # React DOM entrypoint
│   └── package.json
└── README.md
```

# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from llm import ask_llm, get_token_usage
from context_builder import build_context
from token_monitor import log_request, get_stats, get_recent_logs, clear_logs
from hallucination import detect_hallucination
from memory import (
    get_history,
    add_to_history,
    clear_history,
    get_all_sessions,
    format_history_for_display
)
import os
import time

load_dotenv()

app = FastAPI(
    title      = "RAG Chatbot API",
    description= "RAG chatbot with Groq LLM, FAISS, memory, hallucination detection",
    version    = "1.0.0"
)

# ── Models ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question  : str
    session_id: str = "default"

class ChatResponse(BaseModel):
    answer             : str
    session_id         : str
    tokens             : dict
    context_used       : bool
    response_time      : float
    hallucination_check: dict

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "RAG Chatbot is running! 🚀",
        "status" : "healthy"
    }

@app.get("/health")
def health():
    return {
        "status"         : "ok",
        "groq_key_loaded": bool(os.getenv("GROQ_API_KEY"))
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        start_time = time.time()

        # ── Step 1: Build context ──────────────────────────────────────────
        built = build_context(
            query      = request.question,
            session_id = request.session_id,
            top_k      = 3
        )
        context = built["context"]
        history = built["history"]

        # ── Step 2: Call LLM ───────────────────────────────────────────────
        answer = ask_llm(
            question = request.question,
            context  = context,
            history  = history
        )

        # ── Step 3: Hallucination check ────────────────────────────────────
        hallucination_check = detect_hallucination(
            question = request.question,
            answer   = answer,
            context  = context
        )

        # ── Step 4: Save to memory ─────────────────────────────────────────
        add_to_history(request.session_id, "user",      request.question)
        add_to_history(request.session_id, "assistant", answer)

        # ── Step 5: Count tokens + log ─────────────────────────────────────
        tokens        = get_token_usage(request.question, answer)
        response_time = round(time.time() - start_time, 3)

        log_request(
            session_id   = request.session_id,
            question     = request.question,
            answer       = answer,
            tokens       = tokens,
            context_used = bool(context),
            response_time= response_time
        )

        return ChatResponse(
            answer             = answer,
            session_id         = request.session_id,
            tokens             = tokens,
            context_used       = bool(context),
            response_time      = response_time,
            hallucination_check= hallucination_check
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Memory Routes ─────────────────────────────────────────────────────────────

@app.get("/history/{session_id}")
def get_chat_history(session_id: str):
    history = format_history_for_display(session_id)
    return {
        "session_id"   : session_id,
        "message_count": len(history),
        "history"      : history
    }

@app.delete("/history/{session_id}")
def delete_history(session_id: str):
    clear_history(session_id)
    return {"message": f"History cleared for: {session_id}"}

@app.get("/sessions")
def list_sessions():
    sessions = get_all_sessions()
    return {"active_sessions": sessions, "count": len(sessions)}

# ── Monitoring Routes ─────────────────────────────────────────────────────────

@app.get("/stats")
def get_token_stats():
    return get_stats()

@app.get("/logs")
def get_logs(limit: int = 10):
    return {"logs": get_recent_logs(limit), "limit": limit}

@app.delete("/logs")
def delete_logs():
    clear_logs()
    return {"message": "All logs cleared"}
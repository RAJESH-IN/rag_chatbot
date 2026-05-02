# token_monitor.py
# Logs every request with token usage to a JSON file
# Helps track API usage, cost, and performance

import json
import os
from datetime import datetime

# Log file location
LOGS_DIR      = "logs"
LOG_FILE_PATH = os.path.join(LOGS_DIR, "token_logs.json")


def ensure_log_file():
    """
    Create logs directory and empty JSON file
    if they don't exist yet.
    """
    # Create logs folder
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
        print(f"✅ Created logs directory")

    # Create empty JSON log file
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "w") as f:
            json.dump([], f)
        print(f"✅ Created log file: {LOG_FILE_PATH}")


def log_request(
    session_id   : str,
    question     : str,
    answer       : str,
    tokens       : dict,
    context_used : bool,
    response_time: float = 0.0
):
    """
    Log a single chat request to JSON file.

    Args:
        session_id    : user session
        question      : what user asked
        answer        : what LLM answered
        tokens        : token counts dict
        context_used  : whether FAISS context was used
        response_time : how long the request took in seconds
    """
    ensure_log_file()

    # Build log entry
    log_entry = {
        "timestamp"    : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session_id"   : session_id,
        "question"     : question,
        "answer_preview": answer[:100] + "..." if len(answer) > 100 else answer,
        "tokens"       : {
            "input_tokens" : tokens.get("input_tokens",  0),
            "output_tokens": tokens.get("output_tokens", 0),
            "total_tokens" : tokens.get("total_tokens",  0)
        },
        "context_used" : context_used,
        "response_time": round(response_time, 3)
    }

    # Read existing logs
    with open(LOG_FILE_PATH, "r") as f:
        logs = json.load(f)

    # Append new entry
    logs.append(log_entry)

    # Write back
    with open(LOG_FILE_PATH, "w") as f:
        json.dump(logs, f, indent=2)

    print(f"📊 Logged — tokens: {tokens.get('total_tokens', 0)} | "
          f"time: {response_time:.2f}s | "
          f"context: {context_used}")


def get_stats() -> dict:
    """
    Calculate summary statistics from all logs.
    Returns totals and averages.
    """
    ensure_log_file()

    with open(LOG_FILE_PATH, "r") as f:
        logs = json.load(f)

    if not logs:
        return {
            "total_requests"     : 0,
            "total_tokens"       : 0,
            "average_tokens"     : 0,
            "average_response_time": 0,
            "context_used_count" : 0,
            "sessions"           : []
        }

    # Calculate totals
    total_tokens        = sum(l["tokens"]["total_tokens"]  for l in logs)
    total_input         = sum(l["tokens"]["input_tokens"]  for l in logs)
    total_output        = sum(l["tokens"]["output_tokens"] for l in logs)
    total_response_time = sum(l["response_time"]           for l in logs)
    context_used_count  = sum(1 for l in logs if l["context_used"])
    unique_sessions     = list(set(l["session_id"]         for l in logs))

    return {
        "total_requests"       : len(logs),
        "total_tokens"         : total_tokens,
        "total_input_tokens"   : total_input,
        "total_output_tokens"  : total_output,
        "average_tokens"       : round(total_tokens / len(logs), 1),
        "average_response_time": round(total_response_time / len(logs), 3),
        "context_used_count"   : context_used_count,
        "context_used_percent" : round(context_used_count / len(logs) * 100, 1),
        "unique_sessions"      : unique_sessions,
        "session_count"        : len(unique_sessions)
    }


def get_recent_logs(limit: int = 10) -> list:
    """Get the most recent N log entries."""
    ensure_log_file()

    with open(LOG_FILE_PATH, "r") as f:
        logs = json.load(f)

    # Return last N entries newest first
    return logs[-limit:][::-1]


def clear_logs():
    """Clear all logs — reset to empty."""
    ensure_log_file()
    with open(LOG_FILE_PATH, "w") as f:
        json.dump([], f)
    print("✅ Logs cleared")
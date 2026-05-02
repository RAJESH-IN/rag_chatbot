# memory.py
# Simple in-memory conversation history
# Later we can upgrade this to Redis

# Storage — dictionary of session_id → list of messages
# Example:
# {
#   "user123": [
#       {"role": "user",      "content": "What is RAG?"},
#       {"role": "assistant", "content": "RAG stands for..."},
#   ]
# }

memory_store: dict[str, list] = {}

MAX_HISTORY = 10  # keep last 10 messages per session


def get_history(session_id: str) -> list:
    """
    Get conversation history for a session.
    Returns empty list if session not found.
    """
    return memory_store.get(session_id, [])


def add_to_history(session_id: str, role: str, content: str):
    """
    Add a message to conversation history.

    Args:
        session_id : unique user/session identifier
        role       : "user" or "assistant"
        content    : the message text
    """
    # Create session if not exists
    if session_id not in memory_store:
        memory_store[session_id] = []

    # Add new message
    memory_store[session_id].append({
        "role"   : role,
        "content": content
    })

    # Keep only last MAX_HISTORY messages
    # Prevents context window overflow
    if len(memory_store[session_id]) > MAX_HISTORY:
        memory_store[session_id] = memory_store[session_id][-MAX_HISTORY:]


def clear_history(session_id: str):
    """Clear conversation history for a session."""
    if session_id in memory_store:
        del memory_store[session_id]
        print(f"✅ History cleared for session: {session_id}")


def get_all_sessions() -> list:
    """Return all active session IDs."""
    return list(memory_store.keys())


def format_history_for_display(session_id: str) -> list:
    """
    Format history for API display.
    Returns list of messages with role and content.
    """
    history = get_history(session_id)
    return [
        {
            "role"   : msg["role"],
            "content": msg["content"][:100] + "..."  # truncate for display
            if len(msg["content"]) > 100
            else msg["content"]
        }
        for msg in history
    ]
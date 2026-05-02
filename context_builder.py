# context_builder.py
# Combines memory + retrieved docs into a structured prompt

from retrieval import retrieve_as_context
from memory import get_history


def build_context(query: str, session_id: str, top_k: int = 3) -> dict:
    """
    Build full context for LLM by combining:
    1. Retrieved relevant chunks from FAISS
    2. Conversation history from memory

    Args:
        query      : user's question
        session_id : session identifier for memory
        top_k      : number of chunks to retrieve

    Returns:
        dict with context and history
    """

    # Step 1 — Retrieve relevant chunks from FAISS
    retrieved_context = retrieve_as_context(query, top_k)

    # Step 2 — Get conversation history
    history = get_history(session_id)

    # Step 3 — Log what was retrieved
    if retrieved_context:
        print(f"\n📚 Retrieved context for: '{query}'")
        print(f"{retrieved_context[:200]}...")
    else:
        print(f"\n⚠️  No context retrieved for: '{query}'")

    return {
        "context": retrieved_context,
        "history": history
    }


def build_structured_prompt(query: str, context: str) -> str:
    """
    Build a structured prompt that guides the LLM
    to use context and avoid hallucination.

    Args:
        query   : user's question
        context : retrieved relevant text

    Returns:
        formatted prompt string
    """

    if context:
        prompt = f"""You are a helpful and honest AI assistant.

Use the following context to answer the question accurately.
If the answer is not in the context, say "I don't have enough 
information to answer this accurately."

=== CONTEXT ===
{context}
===============

Question: {query}

Answer:"""
    else:
        prompt = f"""You are a helpful and honest AI assistant.

Answer the following question as accurately as possible.
If you are not sure, say "I am not certain about this."

Question: {query}

Answer:"""

    return prompt
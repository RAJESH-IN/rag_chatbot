# context_builder.py
from retrieval import retrieve_as_context
from memory import get_history

# Try to import web search — optional
try:
    from web_search import search_web
    WEB_SEARCH_AVAILABLE = True
    print("✅ Web search available")
except ImportError:
    WEB_SEARCH_AVAILABLE = False
    print("⚠️  Web search not available — using knowledge base only")


# Keywords that suggest need for live/web data
WEB_NEEDED_KEYWORDS = [
    "weather", "today", "current", "latest", "now",
    "price", "news", "stock", "score", "live",
    "2024", "2025", "2026", "yesterday", "tomorrow",
    "trending", "recent", "update", "breaking"
]


def needs_web_search(query: str) -> bool:
    """
    Decide if query needs web search.
    Returns True if query contains live-data keywords.
    """
    query_lower = query.lower()
    return any(kw in query_lower for kw in WEB_NEEDED_KEYWORDS)


def build_context(query: str, session_id: str, top_k: int = 3) -> dict:
    """
    Build full context for LLM by combining:
    1. Retrieved relevant chunks from FAISS
    2. Web search results (if query needs live data)
    3. Conversation history from memory

    Args:
        query      : user's question
        session_id : session identifier for memory
        top_k      : number of chunks to retrieve

    Returns:
        dict with context, history, source, used_web
    """

    # ── Step 1: Always try FAISS first ────────────────────────────────────
    faiss_context = retrieve_as_context(query, top_k)

    if faiss_context:
        print(f"\n📚 FAISS context found for: '{query}'")
        print(f"Preview: {faiss_context[:150]}...")
    else:
        print(f"\n⚠️  No FAISS context for: '{query}'")

    # ── Step 2: Check if web search needed ────────────────────────────────
    web_context = ""
    used_web    = False

    if WEB_SEARCH_AVAILABLE and needs_web_search(query):
        print(f"🌐 Web search triggered for: '{query}'")
        web_context = search_web(query, max_results=3)
        if web_context:
            used_web = True
            print(f"🌐 Web context found: {web_context[:150]}...")
        else:
            print("🌐 Web search returned nothing")

    # ── Step 3: Combine contexts ──────────────────────────────────────────
    combined_context = ""
    source           = "none"

    if faiss_context and web_context:
        combined_context = (
            f"=== From Knowledge Base ===\n{faiss_context}\n\n"
            f"=== From Web Search ===\n{web_context}"
        )
        source = "both"

    elif faiss_context:
        combined_context = faiss_context
        source           = "knowledge_base"

    elif web_context:
        combined_context = web_context
        source           = "web_search"

    else:
        combined_context = ""
        source           = "none"

    # ── Step 4: Get conversation history ──────────────────────────────────
    history = get_history(session_id)

    print(f"📊 Context source: {source} | History: {len(history)} msgs")

    return {
        "context" : combined_context,
        "history" : history,
        "source"  : source,
        "used_web": used_web
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
If the answer is not clearly in the context, say 
"I don't have enough information to answer this accurately."
Do NOT make up information that is not in the context.

=== CONTEXT ===
{context}
===============

Question: {query}

Answer:"""

    else:
        prompt = f"""You are a helpful and honest AI assistant.

Answer the following question as accurately as possible
using your general knowledge.
If you are not sure about something, say 
"I am not certain about this — please verify."

Question: {query}

Answer:"""

    return prompt
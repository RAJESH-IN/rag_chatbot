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


# ── Keywords that trigger web search ─────────────────────────────────────────
WEB_NEEDED_KEYWORDS = [
    # Time-based
    "today", "yesterday", "tomorrow", "now", "current",
    "latest", "recent", "live", "breaking", "trending",
    "2024", "2025", "2026",

    # People / Positions
    "president", "prime minister", "minister", "ceo",
    "chairman", "governor", "mayor", "chief", "head of",
    "who is", "who are", "who was", "who became",

    # Live data
    "weather", "temperature", "forecast", "rain",
    "price", "cost", "rate", "stock", "crypto",
    "bitcoin", "news", "score", "match", "result",

    # General live queries
    "update", "happened", "announced", "released",
    "launched", "won", "lost", "elected", "appointed"
]

# ── Queries that always need web search ───────────────────────────────────────
FACT_STARTERS = [
    "who is", "who was", "who are", "who became",
    "what is the current", "what is today",
    "when did", "where is", "how much is",
    "what is the latest", "what happened"
]


def needs_web_search(query: str) -> bool:
    """
    Decide if query needs web search.
    Checks keywords AND common fact-query patterns.

    Args:
        query : user's question

    Returns:
        True if web search is needed
    """
    query_lower = query.lower()

    # Check keyword list
    has_keyword = any(kw in query_lower for kw in WEB_NEEDED_KEYWORDS)

    # Check fact-query starters
    is_fact_query = any(
        query_lower.startswith(s) for s in FACT_STARTERS
    )

    result = has_keyword or is_fact_query

    if result:
        print(f"🌐 Web search triggered — keyword={has_keyword}, fact={is_fact_query}")

    return result


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
        print(f"   Preview: {faiss_context[:150]}...")
    else:
        print(f"\n⚠️  No FAISS context for: '{query}'")

    # ── Step 2: Check if web search needed ────────────────────────────────
    web_context = ""
    used_web    = False

    if WEB_SEARCH_AVAILABLE and needs_web_search(query):
        print(f"🌐 Searching web for: '{query}'")
        web_context = search_web(query, max_results=3)

        if web_context:
            used_web = True
            print(f"🌐 Web context found: {web_context[:150]}...")
        else:
            print("🌐 Web search returned nothing useful")
    else:
        if not WEB_SEARCH_AVAILABLE:
            print("⚠️  Web search disabled — package not installed")
        else:
            print("📚 No web search needed for this query")

    # ── Step 3: Combine contexts intelligently ────────────────────────────
    combined_context = ""
    source           = "none"

    if faiss_context and web_context:
        # Both sources available — combine them
        combined_context = (
            f"=== From Knowledge Base ===\n{faiss_context}\n\n"
            f"=== From Web Search ===\n{web_context}"
        )
        source = "both"

    elif faiss_context and not web_context:
        # Only knowledge base
        combined_context = faiss_context
        source           = "knowledge_base"

    elif web_context and not faiss_context:
        # Only web search
        combined_context = web_context
        source           = "web_search"

    else:
        # No context found — LLM uses general knowledge
        combined_context = ""
        source           = "none"

    # ── Step 4: Get conversation history ──────────────────────────────────
    history = get_history(session_id)

    print(f"📊 Final source: {source} | History: {len(history)} messages")

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
        context : retrieved relevant text (FAISS + web combined)

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
If you are not sure about something, clearly say
"I am not certain about this — please verify."

Question: {query}

Answer:"""

    return prompt
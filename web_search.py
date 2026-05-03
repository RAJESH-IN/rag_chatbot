# web_search.py
try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


def search_web(query: str, max_results: int = 3) -> str:
    """
    Search web using DuckDuckGo.
    Returns results as string or empty string on failure.
    """
    if not DDGS_AVAILABLE:
        print("⚠️  duckduckgo_search not installed")
        return ""

    try:
        results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=max_results
            )
            for r in search_results:
                title = r.get("title", "")
                body  = r.get("body",  "")
                if title and body:
                    results.append(f"- {title}: {body}")

        if results:
            context = "\n".join(results)
            print(f"🌐 Web found {len(results)} results")
            return context
        else:
            print("🌐 Web search returned no results")
            return ""

    except Exception as e:
        print(f"⚠️  Web search error: {e}")
        return ""


# ── Test directly ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing web search...")
    result = search_web("What is the weather in Mumbai today?")
    if result:
        print("\n✅ Web search working!")
        print(result[:300])
    else:
        print("\n❌ Web search failed")
from ddgs import DDGS

def search_web(query: str, max_results: int = 3) -> str:
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return ""
        lines = []
        for r in results:
            title = r.get("title", "")
            body  = r.get("body",  "")
            if title and body:
                lines.append(f"- {title}: {body}")
        output = "\n".join(lines)
        print(f"WEB SEARCH OK: {len(lines)} results")
        return output
    except Exception as e:
        print(f"WEB SEARCH ERROR: {e}")
        return ""

if __name__ == "__main__":
    r = search_web("president of India 2025")
    print(r if r else "NO RESULTS")
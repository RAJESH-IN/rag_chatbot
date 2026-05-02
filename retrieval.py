from sentence_transformers import SentenceTransformer
from embeddings import load_index, index_exists, build_and_save_index
import numpy as np

# Same model used for embeddings — must match!
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)

# Load or build index at startup
if index_exists():
    index, chunks = load_index()
else:
    print("⚠️  No index found — building from sample.txt...")
    index, chunks = build_and_save_index()


def retrieve(query: str, top_k: int = 3) -> list[str]:
    """
    Find the most relevant chunks for a given query.

    Args:
        query : user's question
        top_k : number of relevant chunks to return

    Returns:
        list of relevant text chunks
    """
    # Step 1 — Embed the query
    query_embedding = model.encode([query]).astype(np.float32)

    # Step 2 — Search FAISS for nearest neighbours
    distances, indices = index.search(query_embedding, top_k)

    # Step 3 — Fetch the matching chunks
    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:  # -1 means no result found
            results.append({
                "chunk"   : chunks[idx],
                "distance": float(distances[0][i])
            })

    return results


def retrieve_as_context(query: str, top_k: int = 3) -> str:
    """
    Retrieve relevant chunks and format as a single context string
    ready to inject into the LLM prompt.
    """
    results = retrieve(query, top_k)

    if not results:
        return ""

    # Format chunks into readable context
    context_parts = []
    for i, result in enumerate(results, 1):
        context_parts.append(f"{i}. {result['chunk']}")

    context = "\n".join(context_parts)
    return context
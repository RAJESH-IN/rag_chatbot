from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import faiss
import numpy as np
import os
import pickle

load_dotenv()

# Model for creating embeddings — runs locally, no API key needed!
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)

# Where to save our FAISS index
FAISS_INDEX_PATH = "faiss_index.pkl"
CHUNKS_PATH      = "chunks.pkl"


def load_documents(file_path: str) -> list[str]:
    """
    Load a text file and split into chunks.
    Each line becomes one chunk for simplicity.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Clean and filter empty lines
    chunks = [line.strip() for line in lines if line.strip()]
    print(f"✅ Loaded {len(chunks)} chunks from {file_path}")
    return chunks


def create_embeddings(chunks: list[str]) -> np.ndarray:
    """
    Convert text chunks into embedding vectors.
    Returns a numpy array of shape (num_chunks, embedding_dim)
    """
    print("⏳ Creating embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    print(f"✅ Created embeddings — shape: {embeddings.shape}")
    return embeddings


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """
    Build a FAISS index from embeddings.
    IndexFlatL2 = exact search using L2 (Euclidean) distance.
    """
    dimension = embeddings.shape[1]  # embedding size (384 for MiniLM)
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    print(f"✅ FAISS index built — {index.ntotal} vectors stored")
    return index


def save_index(index: faiss.IndexFlatL2, chunks: list[str]):
    """Save FAISS index and chunks to disk."""
    with open(FAISS_INDEX_PATH, "wb") as f:
        pickle.dump(index, f)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print("✅ Index saved to disk")


def load_index():
    """Load FAISS index and chunks from disk."""
    with open(FAISS_INDEX_PATH, "rb") as f:
        index = pickle.load(f)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    print(f"✅ Index loaded — {index.ntotal} vectors")
    return index, chunks


def index_exists() -> bool:
    """Check if FAISS index already exists on disk."""
    return os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CHUNKS_PATH)


def build_and_save_index(file_path: str = "data/sample.txt"):
    """
    Full pipeline:
    Load docs → Create embeddings → Build FAISS → Save
    """
    chunks    = load_documents(file_path)
    embeddings = create_embeddings(chunks)
    index     = build_faiss_index(embeddings)
    save_index(index, chunks)
    return index, chunks

# ── Run this when file is executed directly ──────────────────────────────────
if __name__ == "__main__":
    build_and_save_index("data/sample.txt")
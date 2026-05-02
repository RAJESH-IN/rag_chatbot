# test_retrieval.py
from retrieval import retrieve

print("🔍 Testing retrieval...")
print("=" * 40)

results = retrieve("What is RAG?", top_k=3)

for i, r in enumerate(results, 1):
    print(f"\nResult {i}:")
    print(f"Chunk    : {r['chunk']}")
    print(f"Distance : {r['distance']:.4f}")
    print("-" * 40)

print("\n✅ Retrieval test complete!")
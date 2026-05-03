# test_web.py
from duckduckgo_search import DDGS

print("✅ Package imported successfully!")
print("🔍 Testing search...")

results = []
with DDGS() as ddgs:
    for r in ddgs.text("weather in Mumbai today", max_results=3):
        results.append(r)

if results:
    print(f"✅ Found {len(results)} results!")
    for r in results:
        print(f"\nTitle: {r['title']}")
        print(f"Body : {r['body'][:100]}...")
else:
    print("❌ No results returned")
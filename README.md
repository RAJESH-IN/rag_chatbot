# 🤖 RAG Chatbot

> A production-ready **Retrieval Augmented Generation (RAG)** chatbot built from scratch using FastAPI, Groq LLM, FAISS vector search, DuckDuckGo Web Search, and Streamlit — with short-term memory, hallucination detection, and token monitoring.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLama_3.1-orange?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-purple?style=flat-square)
![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Web_Search-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Streamlit UI  (app.py)                     │
│     Chat Interface · Stats Panel · Source Badges            │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP POST /chat
┌──────────────────────────────▼──────────────────────────────┐
│                FastAPI Backend  (main.py)                   │
│                                                             │
│  ┌─────────────────┐      ┌──────────────────────────────┐  │
│  │   FAISS Search  │      │   DuckDuckGo Web Search      │  │
│  │ (retrieval.py)  │      │   (web_search.py)            │  │
│  │ Local knowledge │      │   Live internet data         │  │
│  └────────┬────────┘      └──────────────┬───────────────┘  │
│           │                              │                  │
│  ┌────────▼──────────────────────────────▼───────────────┐  │
│  │        Context Builder  (context_builder.py)          │  │
│  │  Smart routing:                                       │  │
│  │  "What is FAISS?"     → 📚 Knowledge Base only        │  │
│  │  "President of India" → 🌐 Web Search                 │  │
│  │  "Latest AI news"     → 📚🌐 Both combined            │  │
│  └───────────────────────────┬───────────────────────────┘  │
│                              │                              │
│  ┌───────────────────────────▼───────────────────────────┐  │
│  │           Memory  (memory.py)                         │  │
│  │      Session-based conversation history               │  │
│  └───────────────────────────┬───────────────────────────┘  │
│                              │                              │
│  ┌───────────────────────────▼───────────────────────────┐  │
│  │           Groq LLM  (llm.py)                          │  │
│  │     llama-3.1-8b-instant — free and fast              │  │
│  └───────────────────────────┬───────────────────────────┘  │
│                              │                              │
│  ┌───────────────────────────▼───────────────────────────┐  │
│  │  Hallucination Detection    Token Monitor             │  │
│  │  LOW / MEDIUM / HIGH risk   Logs to JSON              │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **RAG Pipeline** | FAISS vector search retrieves relevant knowledge before answering |
| 🌐 **Live Web Search** | DuckDuckGo search for current events, news, weather, prices |
| 🧠 **Smart Routing** | Auto-detects if query needs knowledge base, web, or both |
| 💾 **Short-term Memory** | Remembers full conversation per session |
| 🔎 **Hallucination Detection** | Rates every answer LOW / MEDIUM / HIGH risk |
| 📊 **Token Monitoring** | Logs every request with tokens, latency, source to JSON |
| 💬 **Streamlit UI** | Clean chat interface with source badges and live stats |
| ⚡ **Groq LLM** | Free fastest LLM API — no OpenAI key needed |
| 📚 **Local Embeddings** | sentence-transformers runs locally — zero API cost |
| 🔌 **REST API** | 10 FastAPI endpoints with auto-generated Swagger docs |

---

## 🧠 Smart Source Routing

The chatbot automatically decides where to get the answer:

| Query Type | Example | Source |
|---|---|---|
| Knowledge base question | "What is FAISS?" | 📚 Knowledge Base |
| People and positions | "President of India?" | 🌐 Web Search |
| Weather and climate | "Weather in Mumbai?" | 🌐 Web Search |
| Latest news | "Latest AI news?" | 🌐 Web Search |
| Mixed topic | "Current AI tools?" | 📚🌐 Both |
| Unknown topic | "Random question?" | 💭 General LLM |

**Keywords that automatically trigger web search:**
```
president, prime minister, ceo, chairman, who is, who was
today, yesterday, tomorrow, current, latest, now, 2025
weather, temperature, forecast, price, stock, crypto, news
score, match, result, won, lost, elected, appointed
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Groq (llama-3.1-8b-instant) | Generate answers — free and fast |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | Convert text to vectors locally |
| **Vector Store** | FAISS by Facebook AI | Fast similarity search |
| **Web Search** | DuckDuckGo Search | Live internet data — completely free |
| **Backend** | FastAPI + Uvicorn | REST API server |
| **Frontend** | Streamlit | Chat UI |
| **Memory** | Python dict | Session conversation history |
| **Monitoring** | tiktoken + JSON | Token counting and logging |
| **Environment** | python-dotenv | Secure API key management |

---

## 📁 Project Structure

```
rag_chatbot/
│
├── 📂 data/
│   └── sample.txt              # Knowledge base — add your documents here
│
├── 📂 logs/
│   └── token_logs.json         # Auto-generated request logs
│
├── app.py                      # Streamlit chat UI
├── main.py                     # FastAPI backend — all routes
├── llm.py                      # Groq LLM integration
├── embeddings.py               # Build FAISS index from documents
├── retrieval.py                # Similarity search against FAISS
├── memory.py                   # Session-based conversation memory
├── context_builder.py          # Smart routing — FAISS + web + memory
├── web_search.py               # DuckDuckGo web search integration
├── token_monitor.py            # Log token usage to JSON file
├── hallucination.py            # Detect and rate hallucination risk
│
├── requirements.txt            # Python dependencies
├── .env                        # API keys — never commit this!
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Free Groq API key from [console.groq.com](https://console.groq.com)

---

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/rag_chatbot.git
cd rag_chatbot
```

### Step 2 — Create virtual environment
```bash
# Create
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment
Create a `.env` file in the project root:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```
> 💡 Get your **free** key at [console.groq.com](https://console.groq.com)

### Step 5 — Add your knowledge base
Edit `data/sample.txt` — one fact per line:
```
Your company is ABC Corp founded in 2010.
ABC Corp provides software development services.
The CEO of ABC Corp is John Smith.
```

### Step 6 — Build the FAISS index
```bash
python embeddings.py
```

### Step 7 — Start FastAPI backend
```bash
uvicorn main:app --reload
```

### Step 8 — Start Streamlit UI (new terminal)
```bash
streamlit run app.py
```

Open browser → `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root — API status |
| `GET` | `/health` | Health check |
| `POST` | `/chat` | Send a message — main endpoint |
| `GET` | `/history/{session_id}` | Get conversation history |
| `DELETE` | `/history/{session_id}` | Clear conversation history |
| `GET` | `/sessions` | List all active sessions |
| `GET` | `/stats` | Token usage statistics |
| `GET` | `/logs?limit=10` | Recent request logs |
| `DELETE` | `/logs` | Clear all logs |
| `GET` | `/docs` | Interactive Swagger API docs |

### Example — POST /chat

**Request:**
```json
{
  "question"  : "Who is the president of India?",
  "session_id": "user123"
}
```

**Response:**
```json
{
  "answer"      : "The President of India is Droupadi Murmu...",
  "session_id"  : "user123",
  "context_used": true,
  "source"      : "web_search",
  "response_time": 2.341,
  "tokens": {
    "input_tokens" : 45,
    "output_tokens": 120,
    "total_tokens" : 165
  },
  "hallucination_check": {
    "hallucination_risk": "LOW",
    "confidence_score"  : 0.8,
    "warning"           : null
  }
}
```

---

## 🔎 Hallucination Detection

Every answer is automatically rated for reliability:

| Risk | Meaning | What to Do |
|---|---|---|
| 🟢 **LOW** | Answer grounded in retrieved context | Trust the answer |
| 🟡 **MEDIUM** | Partially grounded — may have gaps | Verify if important |
| 🔴 **HIGH** | Not grounded — may be unreliable | Always verify independently |

**Scoring logic:**
1. Word overlap between answer and context
2. Uncertainty phrase check — "I am not sure" = honest = good
3. Risk phrase check — "I believe", "probably" = risky
4. Context usage check — was context ignored?
5. Final confidence score from 0.0 to 1.0

---

## 📊 Token Monitoring

Every request is logged to `logs/token_logs.json`:

```json
{
  "timestamp"    : "2025-05-04 10:15:23",
  "session_id"   : "raj123",
  "question"     : "Who is the president of India?",
  "answer_preview": "The President of India is Droupadi Murmu...",
  "tokens": {
    "input_tokens" : 45,
    "output_tokens": 120,
    "total_tokens" : 165
  },
  "context_used" : true,
  "response_time": 2.341
}
```

View live stats at `GET /stats`

---

## 🧩 How RAG + Web Works

```
1. INDEXING (one time)
   Documents → Split → Embed with MiniLM → Store in FAISS

2. SMART ROUTING (every query)
   Contains live keywords?
   YES → DuckDuckGo web search
   NO  → FAISS similarity search
   BOTH available → Combine contexts

3. AUGMENTATION
   Context + History → Structured LLM prompt

4. GENERATION
   Groq LLM → Answer → Hallucination check → Log tokens
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `GROQ_API_KEY not found` | Check `.env` file has the key |
| `Model decommissioned` | Update MODEL in `llm.py` — check [Groq docs](https://console.groq.com/docs/deprecations) |
| `FileNotFoundError: sample.txt` | Run `mkdir data` then create `data/sample.txt` |
| `Cannot connect to API` | Start FastAPI first: `uvicorn main:app --reload` |
| `faiss_index.pkl not found` | Run `python embeddings.py` first |
| `Web search not working` | Run `pip install duckduckgo-search` |
| `DDGS missing argument error` | Replace `web_search.py` — API changed in v8.x |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |

---

## 📋 requirements.txt

```
fastapi
uvicorn
groq
faiss-cpu
sentence-transformers
streamlit
tiktoken
python-dotenv
httpx
duckduckgo-search
```

---

## 🔮 Future Improvements

- [ ] Upgrade memory to Redis for persistence across restarts
- [ ] Add PDF and Word document upload support
- [ ] User authentication and multi-user support
- [ ] Deploy on Render or Railway cloud platform
- [ ] Semantic hallucination scoring with embeddings
- [ ] Multi-language document and query support
- [ ] Response streaming word by word
- [ ] Voice input and output support

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

**Rajesh Kumar Mahto**
- Senior Software Engineer — 11 years experience
- Skills: Java · C# · Python · Angular · Azure · AI/ML
- Built with ❤️ as a hands-on AI learning project

---

## ⭐ Support This Project

If this helped you — give it a ⭐ on GitHub!
It helps others discover this project.

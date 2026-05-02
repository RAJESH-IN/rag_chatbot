# 🤖 RAG Chatbot

> A production-ready **Retrieval Augmented Generation (RAG)** chatbot built from scratch using FastAPI, Groq LLM, FAISS vector search, and Streamlit — with short-term memory, hallucination detection, and token monitoring.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat-square&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📸 Screenshots

> **Chat Interface** — Ask questions, see risk indicators, token usage, and response time on every answer.

```
┌─────────────────────────────────────────────────────────┐
│  🤖 RAG Chatbot                                         │
│  Powered by Groq LLM · FAISS · Memory · Hallucination  │
├──────────────────────────────┬──────────────────────────┤
│  💬 Chat                     │  📊 Session Stats        │
│                              │  Messages:  12           │
│  You: What is FAISS?         │  Tokens:    1,450        │
│                              │                          │
│  Bot: FAISS is a library     │  🌐 Overall Stats        │
│  developed by Facebook for   │  Total Requests: 24      │
│  efficient similarity search │  Avg Tokens: 145         │
│                              │  Avg Response: 1.2s      │
│  🟢 Risk: LOW                │  Context Used: 87%       │
│  🪙 Tokens: 145              │                          │
│  ⚡ Time: 1.2s               │  ⚙️ Controls             │
│  📚 Grounded in knowledge    │  [🗑️ Clear Chat]         │
│                              │  [🔄 New Session]        │
│  Ask me anything...          │                          │
└──────────────────────────────┴──────────────────────────┘
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Streamlit UI  (app.py)                     │
│        Chat Interface · Stats Panel · Risk Badges       │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP POST /chat
┌──────────────────────────▼──────────────────────────────┐
│              FastAPI Backend  (main.py)                 │
│                                                         │
│  ┌───────────────┐          ┌───────────────────────┐   │
│  │  FAISS Search  │          │   Memory Store        │   │
│  │ (retrieval.py) │          │   (memory.py)         │   │
│  │                │          │                       │   │
│  │ sentence-      │          │ Session-based         │   │
│  │ transformers   │          │ conversation history  │   │
│  └───────┬────────┘          └──────────┬────────────┘   │
│          │                              │                │
│  ┌───────▼──────────────────────────────▼────────────┐   │
│  │         Context Builder  (context_builder.py)     │   │
│  │    Combines retrieved chunks + history into       │   │
│  │    a structured, grounded LLM prompt              │   │
│  └───────────────────────┬───────────────────────────┘   │
│                          │                              │
│  ┌───────────────────────▼───────────────────────────┐   │
│  │              Groq LLM  (llm.py)                   │   │
│  │         llama-3.1-8b-instant  (free & fast)       │   │
│  └───────────────────────┬───────────────────────────┘   │
│                          │                              │
│  ┌───────────────────────▼───────────────────────────┐   │
│  │      Hallucination Detection  (hallucination.py)  │   │
│  │      Token Monitor  (token_monitor.py)            │   │
│  │      Logs every request → logs/token_logs.json    │   │
│  └───────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **RAG Pipeline** | FAISS vector search retrieves relevant knowledge before answering |
| 🧠 **Short-term Memory** | Remembers full conversation per session |
| 🔎 **Hallucination Detection** | Rates every answer LOW / MEDIUM / HIGH risk |
| 📊 **Token Monitoring** | Logs every request with token count, latency, session to JSON |
| 💬 **Streamlit UI** | Clean chat interface with live stats panel |
| ⚡ **Groq LLM** | Free, fastest LLM API — no OpenAI key needed |
| 📚 **Local Embeddings** | sentence-transformers runs locally — no API cost |
| 🔌 **REST API** | 8 FastAPI endpoints with auto-generated docs |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Groq (llama-3.1-8b-instant) | Generate answers — free & fast |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | Convert text to vectors locally |
| **Vector Store** | FAISS (Facebook AI) | Fast similarity search |
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
├── context_builder.py          # Build structured prompts for LLM
├── token_monitor.py            # Log token usage to JSON file
├── hallucination.py            # Detect and rate hallucination risk
│
├── requirements.txt            # Python dependencies
├── .env                        # API keys (never commit this!)
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

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
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
> 💡 Get your **free** Groq API key at [console.groq.com](https://console.groq.com)

### Step 5 — Add your knowledge base
Edit `data/sample.txt` — add one fact/sentence per line:
```
Your company name is ACME Corp founded in 1990.
ACME Corp provides cloud consulting services.
The CEO of ACME Corp is John Smith.
```

### Step 6 — Build the FAISS index
```bash
python embeddings.py
```
Expected output:
```
✅ Loaded 15 chunks from data/sample.txt
⏳ Creating embeddings...
✅ Created embeddings — shape: (15, 384)
✅ FAISS index built — 15 vectors stored
✅ Index saved to disk
```

### Step 7 — Start FastAPI backend
```bash
uvicorn main:app --reload
```
API running at: `http://127.0.0.1:8000`
API docs at: `http://127.0.0.1:8000/docs`

### Step 8 — Start Streamlit UI
Open a **new terminal** (keep FastAPI running):
```bash
streamlit run app.py
```
Chat UI opens at: `http://localhost:8501`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root — API status |
| `GET` | `/health` | Health check — Groq key loaded |
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
  "question": "What is FAISS?",
  "session_id": "user123"
}
```

**Response:**
```json
{
  "answer": "FAISS is a library developed by Facebook for efficient similarity search...",
  "session_id": "user123",
  "context_used": true,
  "response_time": 1.243,
  "tokens": {
    "input_tokens": 45,
    "output_tokens": 120,
    "total_tokens": 165
  },
  "hallucination_check": {
    "hallucination_risk": "LOW",
    "confidence_score": 0.8,
    "warning": null
  }
}
```

---

## 🔎 Hallucination Detection

Every answer is automatically rated for reliability:

| Risk Level | Meaning | What to Do |
|---|---|---|
| 🟢 **LOW** | Answer grounded in knowledge base | Trust the answer |
| 🟡 **MEDIUM** | Partially grounded — may have gaps | Verify if important |
| 🔴 **HIGH** | Not grounded — may be unreliable | Always verify independently |

**How it works:**
1. **Word overlap check** — how many answer words appear in retrieved context
2. **Uncertainty phrase check** — did LLM say "I'm not sure"? (honest = good)
3. **Risk phrase check** — did LLM say "I believe" or "probably"? (risky)
4. **Context usage check** — was context provided but seemingly ignored?
5. **Confidence score** — combines all checks into 0.0–1.0 score

---

## 📊 Token Monitoring

Every request is logged to `logs/token_logs.json`:

```json
{
  "timestamp": "2025-04-25 10:15:23",
  "session_id": "raj123",
  "question": "What is FAISS?",
  "answer_preview": "FAISS is a library developed by Facebook...",
  "tokens": {
    "input_tokens": 45,
    "output_tokens": 120,
    "total_tokens": 165
  },
  "context_used": true,
  "response_time": 1.243
}
```

View live stats at: `GET /stats`

---

## 🧠 How RAG Works

```
1. INDEXING (one time)
   Your documents → Split into chunks → Embed with MiniLM
   → Store vectors in FAISS index

2. RETRIEVAL (every query)
   User question → Embed question → FAISS similarity search
   → Return top 3 most relevant chunks

3. AUGMENTATION
   Retrieved chunks + Conversation history
   → Build structured prompt for LLM

4. GENERATION
   Groq LLM reads structured prompt
   → Generates answer grounded in YOUR data
   → Not hallucinated from general training
```

---

## 🔮 Future Improvements

- [ ] **Redis memory** — persistent conversation history across restarts
- [ ] **PDF upload** — drag and drop documents to add to knowledge base
- [ ] **User authentication** — multi-user support with login
- [ ] **Deploy on Render / Railway** — one-click cloud deployment
- [ ] **Advanced hallucination** — semantic similarity scoring with embeddings
- [ ] **Multi-language** — support non-English documents and questions
- [ ] **Re-ranking** — improve retrieval quality with cross-encoder
- [ ] **Streaming** — stream LLM response word by word

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `GROQ_API_KEY not found` | Check your `.env` file has the key |
| `Model decommissioned error` | Update MODEL in `llm.py` — check [Groq docs](https://console.groq.com/docs/deprecations) |
| `FileNotFoundError: sample.txt` | Run `mkdir data` then create `data/sample.txt` |
| `Cannot connect to API` | Make sure FastAPI is running: `uvicorn main:app --reload` |
| `faiss_index.pkl not found` | Run `python embeddings.py` first |
| `Port 8501 in use` | Run `streamlit run app.py --server.port 8502` |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

**Rajesh Kumar Mahto**
- Senior Software Engineer — 11 years experience
- Built with ❤️ as a learning project

---

## ⭐ If this helped you

Give it a ⭐ on GitHub — it helps others find this project!


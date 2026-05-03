# app.py
# Streamlit Chat UI for RAG Chatbot

import streamlit as st
import requests
import uuid

# ── Config ────────────────────────────────────────────────────────────────────
API_URL    = "http://127.0.0.1:8000"
PAGE_TITLE = "RAG Chatbot 🤖"

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = PAGE_TITLE,
    page_icon  = "🤖",
    layout     = "wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
        color: #1F3864;
    }
    .sub-header {
        text-align: center;
        color: gray;
        margin-bottom: 1rem;
    }
    .source-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-top: 4px;
    }
    .source-kb  { background:#e8f5e9; color:#2e7d32; }
    .source-web { background:#e3f2fd; color:#1565c0; }
    .source-both{ background:#f3e5f5; color:#6a1b9a; }
    .source-none{ background:#f5f5f5; color:#757575; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages"       not in st.session_state:
    st.session_state.messages       = []

if "session_id"     not in st.session_state:
    st.session_state.session_id     = str(uuid.uuid4())[:8]

if "total_tokens"   not in st.session_state:
    st.session_state.total_tokens   = 0

if "request_count"  not in st.session_state:
    st.session_state.request_count  = 0


# ── Helper functions ──────────────────────────────────────────────────────────

def send_message(question: str) -> dict:
    """Send question to FastAPI and return full response."""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "question"  : question,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        return {
            "error": "❌ Cannot connect to API. Is FastAPI running?\n"
                     "Run: uvicorn main:app --reload"
        }
    except requests.exceptions.Timeout:
        return {"error": "⏱️ Request timed out. Please try again."}
    except Exception as e:
        return {"error": str(e)}


def get_api_stats() -> dict:
    """Fetch overall stats from FastAPI."""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        return response.json()
    except:
        return {}


def check_api_health() -> bool:
    """Check if FastAPI server is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False


def risk_icon(risk: str) -> str:
    """Return emoji for risk level."""
    return {
        "LOW"   : "🟢",
        "MEDIUM": "🟡",
        "HIGH"  : "🔴"
    }.get(risk, "⚪")


def source_label(source: str) -> str:
    """Return readable source label."""
    return {
        "knowledge_base": "📚 Knowledge Base",
        "web_search"    : "🌐 Web Search",
        "both"          : "📚🌐 Knowledge Base + Web",
        "none"          : "💭 General Knowledge"
    }.get(source, "📚 Knowledge Base")


def source_color(source: str) -> str:
    """Return color for source badge."""
    return {
        "knowledge_base": "green",
        "web_search"    : "blue",
        "both"          : "violet",
        "none"          : "gray"
    }.get(source, "green")


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="main-header">🤖 RAG Chatbot</div>',
    unsafe_allow_html=True
)
st.markdown(
    "<p class='sub-header'>"
    "Powered by Groq LLM · FAISS · Short-term Memory · "
    "Hallucination Detection · Web Search"
    "</p>",
    unsafe_allow_html=True
)
st.divider()

# ── Layout ────────────────────────────────────────────────────────────────────
col_chat, col_info = st.columns([2, 1])

# ════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Chat
# ════════════════════════════════════════════════════════════════════════════
with col_chat:

    # ── API Health ────────────────────────────────────────────────────────
    api_ok = check_api_health()
    if api_ok:
        st.success("✅ API Connected — FastAPI is running")
    else:
        st.error(
            "❌ API Offline — Open a new terminal and run:\n"
            "`uvicorn main:app --reload`"
        )
        st.stop()

    # ── Session info ──────────────────────────────────────────────────────
    st.caption(f"🔑 Session ID: `{st.session_state.session_id}`")

    # ── Chat section ──────────────────────────────────────────────────────
    st.subheader("💬 Chat")

    # Display all previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

            # Show metadata only for assistant messages
            if msg["role"] == "assistant" and "meta" in msg:
                meta = msg["meta"]

                risk   = meta.get("hallucination_risk", "UNKNOWN")
                tokens = meta.get("total_tokens",       0)
                time_  = meta.get("response_time",      0)
                source = meta.get("source",             "knowledge_base")

                # ── Metadata row ──────────────────────────────────────────
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.caption(f"{risk_icon(risk)} **{risk}** risk")
                with c2:
                    st.caption(f"🪙 **{tokens}** tokens")
                with c3:
                    st.caption(f"⚡ **{time_}s**")
                with c4:
                    st.caption(source_label(source))

                # ── Warning if needed ─────────────────────────────────────
                warning = meta.get("warning")
                if warning:
                    st.warning(warning)

    # ── Chat input ────────────────────────────────────────────────────────
    if question := st.chat_input("Ask me anything..."):

        # Show user message immediately
        with st.chat_message("user"):
            st.write(question)

        # Save user message
        st.session_state.messages.append({
            "role"   : "user",
            "content": question
        })

        # Get response from API
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                result = send_message(question)

            # ── Handle error ──────────────────────────────────────────────
            if "error" in result:
                st.error(result["error"])
                st.stop()

            # ── Extract response data ─────────────────────────────────────
            answer        = result.get("answer",        "No answer received")
            h_check       = result.get("hallucination_check", {})
            risk          = h_check.get("hallucination_risk", "UNKNOWN")
            warning       = h_check.get("warning")
            tokens_dict   = result.get("tokens",        {})
            total_tokens  = tokens_dict.get("total_tokens",   0)
            response_time = result.get("response_time", 0)
            source        = result.get("source",        "knowledge_base")
            context_used  = result.get("context_used",  False)

            # ── Show answer ───────────────────────────────────────────────
            st.write(answer)

            # ── Show metadata row ─────────────────────────────────────────
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.caption(f"{risk_icon(risk)} **{risk}** risk")
            with c2:
                st.caption(f"🪙 **{total_tokens}** tokens")
            with c3:
                st.caption(f"⚡ **{response_time}s**")
            with c4:
                st.caption(source_label(source))

            # ── Source badge ──────────────────────────────────────────────
            color = source_color(source)
            st.markdown(
                f":{color}[{source_label(source)}]"
            )

            # ── Warning ───────────────────────────────────────────────────
            if warning:
                st.warning(warning)

            # ── Update session counters ───────────────────────────────────
            st.session_state.total_tokens  += total_tokens
            st.session_state.request_count += 1

            # ── Save assistant message to history ─────────────────────────
            st.session_state.messages.append({
                "role"   : "assistant",
                "content": answer,
                "meta"   : {
                    "hallucination_risk": risk,
                    "warning"           : warning,
                    "total_tokens"      : total_tokens,
                    "response_time"     : response_time,
                    "source"            : source,
                    "context_used"      : context_used
                }
            })

        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Info Panel
# ════════════════════════════════════════════════════════════════════════════
with col_info:

    # ── Session Stats ─────────────────────────────────────────────────────
    st.subheader("📊 Session Stats")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(
            label = "Messages",
            value = st.session_state.request_count
        )
    with col_b:
        st.metric(
            label = "Tokens Used",
            value = st.session_state.total_tokens
        )

    # ── Overall Stats ─────────────────────────────────────────────────────
    st.subheader("🌐 Overall Stats")
    stats = get_api_stats()

    if stats and stats.get("total_requests", 0) > 0:
        st.metric(
            label = "Total Requests",
            value = stats.get("total_requests", 0)
        )
        st.metric(
            label = "Total Tokens",
            value = stats.get("total_tokens", 0)
        )
        st.metric(
            label = "Avg Tokens / Request",
            value = stats.get("average_tokens", 0)
        )
        st.metric(
            label = "Avg Response Time",
            value = f"{stats.get('average_response_time', 0)}s"
        )
        st.metric(
            label = "Context Used",
            value = f"{stats.get('context_used_percent', 0)}%"
        )
    else:
        st.info("No stats yet — send a message!")

    st.divider()

    # ── Controls ──────────────────────────────────────────────────────────
    st.subheader("⚙️ Controls")

    # Clear chat history
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages      = []
        st.session_state.total_tokens  = 0
        st.session_state.request_count = 0
        try:
            requests.delete(
                f"{API_URL}/history/{st.session_state.session_id}",
                timeout=5
            )
        except:
            pass
        st.success("✅ Chat cleared!")
        st.rerun()

    # Start new session
    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.messages      = []
        st.session_state.session_id    = str(uuid.uuid4())[:8]
        st.session_state.total_tokens  = 0
        st.session_state.request_count = 0
        st.success("✅ New session started!")
        st.rerun()

    # Clear all logs
    if st.button("📋 Clear Logs", use_container_width=True):
        try:
            requests.delete(f"{API_URL}/logs", timeout=5)
            st.success("✅ Logs cleared!")
        except:
            st.error("Could not clear logs")

    st.divider()

    # ── How It Works ──────────────────────────────────────────────────────
    st.subheader("ℹ️ How It Works")
    st.markdown("""
    1. 📝 You ask a question
    2. 🔍 FAISS searches knowledge base
    3. 🌐 Web search for live queries
    4. 🧠 Memory adds chat history
    5. 🤖 Groq LLM generates answer
    6. 🔎 Hallucination check rates it
    7. 📊 Token monitor logs everything
    """)

    st.divider()

    # ── Risk Legend ───────────────────────────────────────────────────────
    st.subheader("🎯 Risk Legend")
    st.markdown("""
    - 🟢 **LOW** — Grounded in context
    - 🟡 **MEDIUM** — Partially grounded
    - 🔴 **HIGH** — May be unreliable
    """)

    st.divider()

    # ── Source Legend ─────────────────────────────────────────────────────
    st.subheader("📡 Source Legend")
    st.markdown("""
    - 📚 **Knowledge Base** — from your documents
    - 🌐 **Web Search** — from live internet
    - 📚🌐 **Both** — combined sources
    - 💭 **General** — LLM general knowledge
    """)
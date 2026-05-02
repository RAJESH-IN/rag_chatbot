# app.py
# Streamlit Chat UI for RAG Chatbot

import streamlit as st
import requests
import json

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
    .risk-low    { color: #28a745; font-weight: bold; }
    .risk-medium { color: #ffc107; font-weight: bold; }
    .risk-high   { color: #dc3545; font-weight: bold; }
    .metric-box  {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .stChatMessage { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)


# ── Session state — persists across reruns ────────────────────────────────────
if "messages"   not in st.session_state:
    st.session_state.messages    = []  # chat history for display

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id  = str(uuid.uuid4())[:8]  # unique session

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

if "request_count" not in st.session_state:
    st.session_state.request_count = 0


# ── Helper functions ──────────────────────────────────────────────────────────

def send_message(question: str) -> dict:
    """Send question to FastAPI and return response."""
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
        return {"error": "Cannot connect to API. Is the FastAPI server running?"}
    except Exception as e:
        return {"error": str(e)}


def get_stats() -> dict:
    """Fetch stats from FastAPI."""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        return response.json()
    except:
        return {}


def check_api_health() -> bool:
    """Check if FastAPI is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False


def risk_color(risk: str) -> str:
    """Return color based on risk level."""
    colors = {
        "LOW"   : "🟢",
        "MEDIUM": "🟡",
        "HIGH"  : "🔴"
    }
    return colors.get(risk, "⚪")


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="main-header">🤖 RAG Chatbot</div>',
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "Powered by Groq LLM · FAISS · Short-term Memory · Hallucination Detection"
    "</p>",
    unsafe_allow_html=True
)
st.divider()

# ── Layout — two columns ──────────────────────────────────────────────────────
col_chat, col_info = st.columns([2, 1])

# ════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Chat
# ════════════════════════════════════════════════════════════════════════════
with col_chat:

    # API status
    api_ok = check_api_health()
    if api_ok:
        st.success("✅ API Connected — FastAPI is running")
    else:
        st.error("❌ API Offline — Start FastAPI: uvicorn main:app --reload")
        st.stop()

    # Session info
    st.caption(f"🔑 Session ID: `{st.session_state.session_id}`")

    # ── Chat history display ──────────────────────────────────────────────
    st.subheader("💬 Chat")

    # Display all previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

            # Show metadata for assistant messages
            if msg["role"] == "assistant" and "meta" in msg:
                meta = msg["meta"]
                risk = meta.get("hallucination_risk", "UNKNOWN")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(
                        f"{risk_color(risk)} Risk: **{risk}**"
                    )
                with col2:
                    st.caption(
                        f"🪙 Tokens: **{meta.get('total_tokens', 0)}**"
                    )
                with col3:
                    st.caption(
                        f"⚡ Time: **{meta.get('response_time', 0)}s**"
                    )

                # Show warning if high/medium risk
                warning = meta.get("warning")
                if warning:
                    st.warning(warning)

                # Show context used
                if meta.get("context_used"):
                    st.caption("📚 Answer grounded in knowledge base")

    # ── Chat input ────────────────────────────────────────────────────────
    if question := st.chat_input("Ask me anything..."):

        # Show user message
        with st.chat_message("user"):
            st.write(question)

        # Add to display history
        st.session_state.messages.append({
            "role"   : "user",
            "content": question
        })

        # Call API
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                result = send_message(question)

            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                answer = result.get("answer", "No answer received")
                st.write(answer)

                # Extract metadata
                h_check       = result.get("hallucination_check", {})
                risk          = h_check.get("hallucination_risk", "UNKNOWN")
                confidence    = h_check.get("confidence_score",   0)
                warning       = h_check.get("warning")
                tokens        = result.get("tokens",         {})
                total_tokens  = tokens.get("total_tokens",   0)
                response_time = result.get("response_time",  0)
                context_used  = result.get("context_used",   False)

                # Show metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"{risk_color(risk)} Risk: **{risk}**")
                with col2:
                    st.caption(f"🪙 Tokens: **{total_tokens}**")
                with col3:
                    st.caption(f"⚡ Time: **{response_time}s**")

                if warning:
                    st.warning(warning)

                if context_used:
                    st.caption("📚 Answer grounded in knowledge base")

                # Update session stats
                st.session_state.total_tokens  += total_tokens
                st.session_state.request_count += 1

                # Save to display history
                st.session_state.messages.append({
                    "role"   : "assistant",
                    "content": answer,
                    "meta"   : {
                        "hallucination_risk": risk,
                        "confidence_score"  : confidence,
                        "warning"           : warning,
                        "total_tokens"      : total_tokens,
                        "response_time"     : response_time,
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

    # ── Overall Stats from API ────────────────────────────────────────────
    st.subheader("🌐 Overall Stats")
    stats = get_stats()

    if stats:
        st.metric("Total Requests",   stats.get("total_requests",        0))
        st.metric("Total Tokens",     stats.get("total_tokens",          0))
        st.metric("Avg Tokens/Req",   stats.get("average_tokens",        0))
        st.metric("Avg Response Time",
                  f"{stats.get('average_response_time', 0)}s")
        st.metric("Context Used",
                  f"{stats.get('context_used_percent', 0)}%")
    else:
        st.info("No stats yet — send a message!")

    st.divider()

    # ── Controls ──────────────────────────────────────────────────────────
    st.subheader("⚙️ Controls")

    # Clear chat
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        try:
            requests.delete(
                f"{API_URL}/history/{st.session_state.session_id}"
            )
        except:
            pass
        st.success("Chat cleared!")
        st.rerun()

    # New session
    if st.button("🔄 New Session", use_container_width=True):
        import uuid
        st.session_state.messages      = []
        st.session_state.session_id    = str(uuid.uuid4())[:8]
        st.session_state.total_tokens  = 0
        st.session_state.request_count = 0
        st.success("New session started!")
        st.rerun()

    st.divider()

    # ── How it works ──────────────────────────────────────────────────────
    st.subheader("ℹ️ How It Works")
    st.markdown("""
    1. 📝 **Your question** goes to FastAPI
    2. 🔍 **FAISS** finds relevant knowledge
    3. 🧠 **Memory** adds conversation history
    4. 🤖 **Groq LLM** generates the answer
    5. 🔎 **Hallucination check** rates reliability
    6. 📊 **Token monitor** logs everything
    """)

    # ── Risk Legend ───────────────────────────────────────────────────────
    st.subheader("🎯 Risk Legend")
    st.markdown("""
    - 🟢 **LOW** — Answer grounded in data
    - 🟡 **MEDIUM** — Partially grounded
    - 🔴 **HIGH** — May be unreliable
    """)
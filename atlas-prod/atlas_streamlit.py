"""
ATLAS AI — Streamlit frontend (observatory / star-chart theme)
"""

import os
import requests
import streamlit as st

API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="ATLAS AI",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0a0e17;
    --panel: #141a26;
    --border: #1e2738;
    --text: #e8edf7;
    --muted: #6f7a92;
    --amber: #ffb454;
    --cyan: #5ec8d8;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text);
}

.main { background: var(--bg); }

.main::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
    background-size: 64px 64px;
    opacity: 0.18;
    pointer-events: none;
    z-index: 0;
}

section[data-testid="stSidebar"] {
    background: #0d1320;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

.atlas-header {
    display: flex;
    align-items: baseline;
    gap: 14px;
    padding: 1.4rem 0 1rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.6rem;
    position: relative;
    z-index: 1;
}
.atlas-header h1 {
    font-weight: 700;
    font-size: 1.9rem;
    letter-spacing: -0.02em;
    margin: 0;
    color: var(--text);
}
.atlas-header .coord {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--cyan);
    letter-spacing: 0.08em;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 3px 9px;
    background: rgba(94, 200, 216, 0.06);
}
.atlas-header .sub {
    font-size: 0.85rem;
    color: var(--muted);
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
}

.tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 6px;
    display: inline-block;
    padding: 1px 7px;
    border-radius: 3px;
}
.tag-q { color: var(--amber); border: 1px solid rgba(255,180,84,0.35); background: rgba(255,180,84,0.06); }
.tag-a { color: var(--cyan); border: 1px solid rgba(94,200,216,0.35); background: rgba(94,200,216,0.06); }

.source-block {
    background: var(--panel);
    border: 1px solid var(--border);
    border-left: 2px solid var(--cyan);
    border-radius: 4px;
    padding: 0.6rem 0.85rem;
    margin: 6px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #aab4cc;
}
.source-block .source-tag {
    color: var(--cyan);
    font-weight: 500;
    display: block;
    margin-bottom: 3px;
}

section[data-testid="stSidebar"] input[type="password"],
section[data-testid="stSidebar"] input[type="text"] {
    background: #f4f6fb !important;
    color: #1a1f2e !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] input::placeholder {
    color: #8a93ad !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #f4f6fb !important;
    color: #1a1f2e !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #1a1f2e !important;
}

[data-testid="stChatInput"] {
    background: #f4f6fb !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}
[data-testid="stChatInput"] textarea {
    background: #f4f6fb !important;
    border: none !important;
    color: #1a1f2e !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #8a93ad !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--amber) !important;
}

div[data-testid="stButton"] > button {
    background: var(--panel) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: var(--cyan) !important;
}

[data-testid="stChatMessage"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    position: relative;
    z-index: 1;
}

.stSpinner > div { color: var(--amber) !important; }

.status-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    padding: 2px 9px;
    border-radius: 99px;
    border: 1px solid var(--border);
    display: inline-block;
}
.status-ok { color: #7ee787; border-color: rgba(126,231,135,0.3); background: rgba(126,231,135,0.06); }
.status-err { color: #ff6b6b; border-color: rgba(255,107,107,0.3); background: rgba(255,107,107,0.06); }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Configuration")

    api_key = st.text_input(
        "Anthropic API key",
        type="password",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
        help="Sent per-request, or leave blank if the backend already has ANTHROPIC_API_KEY set.",
    )

    st.markdown("---")
    st.markdown("### Model")

    model_choice = st.selectbox(
        "Model",
        ["claude-sonnet-4-6", "claude-haiku-4-5"],
        index=0,
        label_visibility="collapsed",
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.1)
    top_k = st.slider("Retrieved chunks (top-k)", 1, 10, 5)

    st.markdown("---")

    try:
        h = requests.get(f"{API_URL}/health", timeout=3)
        if h.ok:
            st.markdown('<span class="status-pill status-ok">● backend online</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill status-err">● backend error</span>', unsafe_allow_html=True)
    except requests.RequestException:
        st.markdown('<span class="status-pill status-err">● backend unreachable</span>', unsafe_allow_html=True)

    st.caption(API_URL)

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(f"""
<div class="atlas-header">
  <span style="font-size:1.8rem">🔭</span>
  <h1>ATLAS AI</h1>
  <span class="coord">RAG · KNOWLEDGE CATALOG</span>
  <span class="sub">{len(st.session_state.messages)//2:03d} entries logged</span>
</div>
""", unsafe_allow_html=True)

for i, msg in enumerate(st.session_state.messages):
    idx = i // 2 + 1
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f'<span class="tag tag-q">Q-{idx:03d}</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="tag tag-a">A-{idx:03d}</span>', unsafe_allow_html=True)

        st.markdown(msg["content"])

        if msg.get("sources"):
            with st.expander(f"📡 {len(msg['sources'])} sources"):
                for j, src in enumerate(msg["sources"]):
                    st.markdown(f"""
                    <div class="source-block">
                      <span class="source-tag">[{j+1}] {src['source']}</span>
                      {src['snippet']}…
                    </div>""", unsafe_allow_html=True)

query = st.chat_input("Query the knowledge base…")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    idx = len(st.session_state.messages) // 2 + 1
    with st.chat_message("user"):
        st.markdown(f'<span class="tag tag-q">Q-{idx:03d}</span>', unsafe_allow_html=True)
        st.markdown(query)

    with st.chat_message("assistant"):
        st.markdown(f'<span class="tag tag-a">A-{idx:03d}</span>', unsafe_allow_html=True)
        with st.spinner("Scanning catalog…"):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "query": query,
                        "model": model_choice,
                        "temperature": temperature,
                        "top_k": top_k,
                        "api_key": api_key or None,
                    },
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                answer = data["answer"]
                sources = data["sources"]

                st.markdown(answer)
                if sources:
                    with st.expander(f"📡 {len(sources)} sources"):
                        for j, src in enumerate(sources):
                            st.markdown(f"""
                            <div class="source-block">
                              <span class="source-tag">[{j+1}] {src['source']}</span>
                              {src['snippet']}…
                            </div>""", unsafe_allow_html=True)

            except requests.RequestException as e:
                answer = f"Signal lost — could not reach ATLAS backend.\n\n`{e}`"
                sources = []
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

import html
import re
import textwrap
import time
from typing import Any, Dict, List, Optional

import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

BASE_URL = "http://127.0.0.1:8000"

VIDEO_ENDPOINT = f"{BASE_URL}/videos"
ASK_ENDPOINT = f"{BASE_URL}/ask"
HEALTH_ENDPOINT = f"{BASE_URL}/health"

REQUEST_TIMEOUT = 120
HEALTH_TIMEOUT = 3


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="YouTubeRAG",
    page_icon="🟥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML render helper
# ============================================================
# st.markdown() runs Markdown before HTML, and Markdown treats any
# line indented 4+ spaces as a fenced code block. Dedenting here
# guarantees hand-indented HTML strings still render as real markup.


def render(raw_html: str) -> None:
    """Render a block of raw HTML safely, immune to source indentation."""

    st.markdown(textwrap.dedent(raw_html).strip(), unsafe_allow_html=True)


# ============================================================
# Design System
# ============================================================

render(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700'
        '&family=Work+Sans:wght@400;500;600'
        '&family=IBM+Plex+Mono:wght@400;500;600&display=swap'
    );

    :root {
        --bg-void: #0f0f0f;
        --bg-panel: #212121;
        --bg-raised: #282828;
        --bg-inset: #181818;

        --border: #3f3f3f;
        --border-strong: #717171;

        --text-primary: #f1f1f1;
        --text-secondary: #aaaaaa;
        --text-muted: #717171;

        --accent: #FF0000;
        --accent-strong: #cc0000;
        --accent-soft: rgba(255, 0, 0, 0.14);

        --signal: #3ea6ff;
        --signal-soft: rgba(62, 166, 255, 0.16);

        --recording: #FF0000;

        --radius-lg: 14px;
        --radius-md: 10px;
        --radius-sm: 6px;
    }

    html, body, [class*="css"] {
        font-family: "Work Sans", sans-serif;
    }

    .stApp {
        background: var(--bg-void);
        color: var(--text-primary);
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 8rem;
    }

    ::selection {
        background: var(--accent-soft);
        color: var(--text-primary);
    }

    *:focus-visible {
        outline: 2px solid var(--accent) !important;
        outline-offset: 2px;
    }

    section[data-testid="stSidebar"] {
        background: var(--bg-panel);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem;
    }

    h1, h2, h3 {
        font-family: "Oswald", sans-serif !important;
        color: var(--text-primary) !important;
    }

    h3 {
        font-size: 1.05rem !important;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    .sprocket-rail {
        height: 10px;
        width: 100%;
        background-image: radial-gradient(circle, var(--bg-void) 2.4px, transparent 2.6px);
        background-size: 18px 10px;
        background-position: 6px center;
        background-color: var(--bg-inset);
        border-radius: 3px;
    }

    .chyron {
        border-top: 2px solid var(--accent);
        border-bottom: 1px solid var(--border-strong);
        padding: 1.15rem 0 1.3rem;
        margin-bottom: 1.5rem;
    }

    .chyron-eyebrow {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--accent);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.72rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .chyron-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--signal);
        box-shadow: 0 0 0 3px rgba(74, 133, 119, 0.18);
    }

    .chyron-dot.live {
        background: var(--recording);
        box-shadow: 0 0 0 3px rgba(184, 69, 58, 0.18);
        animation: pulse 1.8s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.35; }
    }

    .chyron-title {
        font-family: "Oswald", sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        line-height: 1.05;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: var(--text-primary);
    }

    .chyron-title span {
        color: var(--accent);
    }

    .chyron-subtitle {
        max-width: 700px;
        margin-top: 0.5rem;
        color: var(--text-secondary);
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .panel {
        background: var(--bg-panel);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        overflow: hidden;
        margin-bottom: 1.1rem;
    }

    .panel-body {
        padding: 1.3rem 1.4rem;
    }

    .panel-label {
        margin-bottom: 0.3rem;
        color: var(--text-muted);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.7rem;
        letter-spacing: 2.2px;
        text-transform: uppercase;
    }

    .panel-title {
        margin-bottom: 0.2rem;
        color: var(--text-primary);
        font-family: "Oswald", sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
    }

    .panel-description {
        color: var(--text-secondary);
        font-size: 0.88rem;
    }

    .reel-tag {
        display: inline-block;
        padding: 0.2rem 0.55rem;
        margin-bottom: 0.6rem;
        color: var(--signal);
        background: var(--signal-soft);
        border: 1px solid rgba(74, 133, 119, 0.4);
        border-radius: 4px;
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.7rem;
        letter-spacing: 2.5px;
        text-transform: uppercase;
    }

    .reel-heading {
        color: var(--text-primary);
        font-family: "Oswald", sans-serif;
        font-size: 1.35rem;
        font-weight: 600;
    }

    .cartridge {
        margin: 0.9rem 0;
        overflow: hidden;
        background: var(--bg-raised);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-md);
    }

    .cartridge-body {
        padding: 0.85rem 1rem 1rem;
    }

    .cartridge-label {
        color: var(--accent);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .cartridge-url {
        margin-top: 0.4rem;
        color: var(--text-secondary);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.78rem;
        line-height: 1.5;
        word-break: break-all;
    }

    .empty-slate {
        padding: 1.1rem 1rem;
        color: var(--text-muted);
        background: var(--bg-inset);
        border: 1px dashed var(--border-strong);
        border-radius: var(--radius-md);
        font-size: 0.85rem;
        line-height: 1.6;
    }

    .sidebar-footnote {
        color: var(--text-muted);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.72rem;
        line-height: 1.6;
        letter-spacing: 0.3px;
    }

    /* ====================================================
       Chat transcript
       ==================================================== */

    .chat-empty {
        padding: 1.4rem 1.5rem;
        margin-top: 0.4rem;
        color: var(--text-muted);
        background: var(--bg-inset);
        border: 1px dashed var(--border-strong);
        border-radius: var(--radius-lg);
        font-size: 0.9rem;
        line-height: 1.7;
    }

    .chat-empty b {
        color: var(--text-secondary);
    }



    [data-testid="stChatInput"] {
        background: var(--bg-panel);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-lg);
    }

    [data-testid="stChatInput"] textarea {
        color: var(--text-primary) !important;
        font-family: "IBM Plex Mono", monospace !important;
    }

    .msg-tag {
        display: inline-block;
        color: var(--accent);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.68rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .msg-tag.user {
        color: var(--signal);
    }

    .msg-body {
        color: var(--text-primary);
        font-size: 0.98rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    .msg-meta-row {
        margin-top: 0.6rem;
        display: flex;
        gap: 1.1rem;
        flex-wrap: wrap;
    }

    .msg-meta-chip {
        color: var(--text-muted);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.7rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .msg-meta-chip b {
        color: var(--text-secondary);
    }

    .frame-card {
        margin-bottom: 0.6rem;
        overflow: hidden;
        background: var(--bg-inset);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
    }

    .frame-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0.9rem 0.35rem;
    }

    .frame-number {
        color: var(--accent);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .frame-code {
        color: var(--text-muted);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.7rem;
        letter-spacing: 1px;
    }

    .frame-text {
        padding: 0.25rem 0.9rem 0.85rem;
        color: var(--text-secondary);
        font-size: 0.87rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        border-radius: var(--radius-sm);
    }

    div[data-baseweb="base-input"] {
        background: var(--bg-inset) !important;
        border-color: var(--border-strong) !important;
    }

    div[data-baseweb="base-input"]:focus-within {
        border-color: var(--accent) !important;
    }

    .stTextInput input {
        color: var(--text-primary) !important;
        font-family: "IBM Plex Mono", monospace !important;
        font-size: 0.9rem !important;
    }

    div.stButton > button {
        min-height: 42px;
        background: var(--bg-raised);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-sm);
        color: var(--text-primary);
        font-family: "Work Sans", sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        color: var(--accent-strong);
        border-color: var(--accent);
        transform: translateY(-1px);
    }

    div.stButton > button[kind="primary"] {
        background: var(--accent);
        border-color: var(--accent);
        color: #16130a;
    }

    div.stButton > button[kind="primary"]:hover {
        background: var(--accent-strong);
        border-color: var(--accent-strong);
        color: #16130a;
    }

    div[data-testid="stMetric"] {
        padding: 0.7rem 0.85rem;
        background: var(--bg-inset);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-family: "IBM Plex Mono", monospace !important;
        font-size: 0.66rem !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: var(--accent) !important;
        font-family: "Oswald", sans-serif !important;
        font-size: 1.5rem !important;
    }

    div[data-testid="stAlert"] {
        background: var(--bg-raised);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-md);
    }

    details {
        background: transparent !important;
        border: none !important;
    }

    summary {
        color: var(--text-secondary) !important;
        font-family: "IBM Plex Mono", monospace !important;
        font-size: 0.78rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .site-footer {
        padding-top: 2rem;
        color: var(--text-muted);
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.7rem;
        letter-spacing: 1.5px;
        text-align: center;
        text-transform: uppercase;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    </style>
    """
)


# ============================================================
# Session State
# ============================================================

DEFAULT_STATE = {
    "video_url": None,
    "chunks": None,
    "ingestion_time": None,
    "messages": [],  # list of {role, content, sources?, latency?}
}


def initialize_state() -> None:
    """Initialize application state once per Streamlit session."""

    for key, default in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default


initialize_state()


def reset_conversation() -> None:
    """Clear chat history, e.g. when a new video is loaded."""

    st.session_state.messages = []


# ============================================================
# API Layer
# ============================================================

def check_backend_health() -> bool:
    """Return True when the FastAPI backend is reachable."""

    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=HEALTH_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False


def _raise_with_body(response: requests.Response) -> None:
    """Raise for non-2xx responses, including the response body for context.

    requests' default raise_for_status() only reports the status code, which
    hides useful info like FastAPI's 422 validation error details.
    """

    if response.status_code >= 400:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise requests.HTTPError(f"{response.status_code} error: {detail}")


def ingest_video(url: str) -> Dict[str, Any]:
    """Send a YouTube URL to the ingestion endpoint."""

    response = requests.post(VIDEO_ENDPOINT, json={"url": url}, timeout=REQUEST_TIMEOUT)
    _raise_with_body(response)
    return response.json()


def ask_question(question: str, chat_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Send a question to the RAG endpoint."""

    payload = {"question": question}
    if chat_history:
        payload["chat_history"] = chat_history

    response = requests.post(ASK_ENDPOINT, json=payload, timeout=REQUEST_TIMEOUT)
    _raise_with_body(response)
    return response.json()


# ============================================================
# Data Helpers
# ============================================================

def parse_chunk_count(message: str) -> Optional[int]:
    """Extract the chunk count from an ingestion response message."""

    if not message:
        return None

    match = re.search(r"(\d+)\s+chunks", message, re.IGNORECASE)
    return int(match.group(1)) if match else None


def format_timecode(seconds: Optional[float]) -> str:
    """Format elapsed seconds as MM:SS.CS."""

    if seconds is None:
        return "—"

    total_ms = max(0, int(seconds * 1000))
    minutes, remainder = divmod(total_ms, 60_000)
    secs, milliseconds = divmod(remainder, 1_000)
    centiseconds = milliseconds // 10

    return f"{minutes:02d}:{secs:02d}.{centiseconds:02d}"


def safe_text(value: Any) -> str:
    """Safely render arbitrary API text inside HTML."""

    return html.escape(str(value or ""))


# ============================================================
# Chat rendering helpers
# ============================================================

def render_user_turn(content: str) -> None:
    with st.chat_message("user"):
        st.markdown(content)


def render_assistant_turn(msg: Dict[str, Any]) -> None:
    raw_content = msg.get("content") or ""
    
    think_match = re.search(r'<think>(.*?)</think>', raw_content, flags=re.DOTALL | re.IGNORECASE)
    think_content = None
    if think_match:
        think_content = think_match.group(1).strip()
        raw_content = re.sub(r'<think>.*?</think>', '', raw_content, flags=re.DOTALL | re.IGNORECASE).strip()

    with st.chat_message("assistant"):
        if think_content:
            with st.expander("Thinking Process", expanded=False):
                st.markdown(think_content)

        st.markdown(raw_content)

        latency = msg.get("latency")
        sources = msg.get("sources") or []

        render(
            f"""
            <div class="msg-meta-row">
                <span class="msg-meta-chip">Latency <b>{
                    f"{latency:.2f}s" if isinstance(latency, (int, float)) else "—"
                }</b></span>
                <span class="msg-meta-chip">Sources <b>{len(sources)}</b></span>
            </div>
            """
        )

        if sources:
            with st.expander(f"Retrieved context ({len(sources)})", expanded=False):
                for index, source in enumerate(sources, start=1):
                    content = source.get("content", "")
                    metadata = source.get("metadata", {})

                    safe_content = safe_text(content)

                    render(
                        f"""
                        <div class="frame-card">
                            <div class="frame-meta">
                                <span class="frame-number">FRAME {index:02d}</span>
                                <span class="frame-code">RETRIEVED · CHUNK {index}</span>
                            </div>
                            <div class="frame-text">{safe_content}</div>
                        </div>
                        """
                    )

                    if metadata:
                        st.caption(f"Metadata · frame {index:02d}")
                        st.json(metadata, expanded=False)


# ============================================================
# Hero
# ============================================================

video_loaded = bool(st.session_state.video_url)

render(
    f"""
    <div class="chyron">
        <div class="chyron-eyebrow">
            <span class="chyron-dot {"live" if video_loaded else ""}"></span>
            {"LIVE KNOWLEDGE BASE" if video_loaded else "AWAITING FOOTAGE"}
        </div>
        <div class="chyron-title">
            Tube<span>RAG</span>
        </div>
        <div class="chyron-subtitle">
            Load a YouTube transcript, then chat with it — grounded,
            timecoded answers pulled straight from the source footage.
        </div>
    </div>
    """
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    render(
        """
        <div class="reel-tag">REEL LOADER</div>
        <div class="reel-heading">Load a video</div>
        """
    )

    st.caption("Paste a YouTube URL to build the knowledge base.")

    video_url_input = st.text_input(
        "YouTube URL",
        placeholder="https://youtube.com/watch?v=...",
        label_visibility="collapsed",
        key="video_url_input",
    )

    process_video = st.button(
        "Process Video",
        type="primary",
        use_container_width=True,
        key="process_video_btn",
    )

    render('<div class="sprocket-rail"></div>')

    render(
        """
        <div class="panel-label" style="margin-top:1.1rem;">
            On the reel now
        </div>
        """
    )

    if st.session_state.video_url:

        current_url = safe_text(st.session_state.video_url)

        render(
            f"""
            <div class="cartridge">
                <div class="sprocket-rail"></div>
                <div class="cartridge-body">
                    <div class="cartridge-label">Active source</div>
                    <div class="cartridge-url">{current_url}</div>
                </div>
            </div>
            """
        )
        
        st.video(current_url)

        metric_col_1, metric_col_2 = st.columns(2)

        with metric_col_1:
            st.metric(
                "Chunks",
                st.session_state.chunks if st.session_state.chunks is not None else "—",
            )

        with metric_col_2:
            st.metric("Indexed in", format_timecode(st.session_state.ingestion_time))

        if st.session_state.messages:
            st.button(
                "Clear conversation",
                use_container_width=True,
                key="clear_chat_btn",
                on_click=reset_conversation,
            )

    else:

        render(
            """
            <div class="empty-slate">
                No footage loaded yet.<br><br>
                Process a video to start the reel
                and unlock the chat.
            </div>
            """
        )

    st.markdown("<br>", unsafe_allow_html=True)

    render(
        """
        <div class="sidebar-footnote">
            ONE ACTIVE VIDEO AT A TIME<br>
            FASTAPI · FAISS · GROQ
        </div>
        """
    )


# ============================================================
# Process Video
# ============================================================

if process_video:

    url = video_url_input.strip()

    if not url:
        st.error("Please paste a YouTube URL first.")

    elif not check_backend_health():
        st.error(f"The RAG API is unreachable. Start the FastAPI server at {BASE_URL}.")

    else:

        with st.spinner("Rolling the transcript into the index..."):

            try:
                started_at = time.perf_counter()
                result = ingest_video(url)
                elapsed = time.perf_counter() - started_at

                chunks = parse_chunk_count(result.get("message", ""))

                st.session_state.video_url = result.get("url") or url
                st.session_state.chunks = chunks
                st.session_state.ingestion_time = elapsed

                reset_conversation()

                st.success("Video processed successfully.")
                st.rerun()

            except requests.RequestException as error:
                st.error(f"Could not connect to the RAG API: {error}")

            except Exception as error:
                st.error(f"Video processing failed: {error}")


# ============================================================
# Chat transcript
# ============================================================

if not st.session_state.messages:
    render(
        """
        <div class="chat-empty">
            <b>Nothing asked yet.</b><br><br>
            Once a video is loaded, ask things like
            "what's the main argument here?" or
            "summarize the last ten minutes" —
            answers stay grounded in the transcript,
            with retrieved chunks you can inspect below each reply.
        </div>
        """
    )
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user_turn(msg["content"])
        else:
            render_assistant_turn(msg)


# ============================================================
# Chat input
# ============================================================

chat_placeholder = (
    "Ask something about the footage..."
    if video_loaded
    else "Load a video in the sidebar first..."
)

question_text = st.chat_input(chat_placeholder, disabled=not video_loaded)

if question_text:

    question_text = question_text.strip()

    if not question_text:
        pass

    elif not check_backend_health():
        st.session_state.messages.append({"role": "user", "content": question_text})
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"The RAG API is unreachable. Start the FastAPI server at {BASE_URL}.",
                "sources": [],
                "latency": None,
            }
        )
        st.rerun()

    else:

        st.session_state.messages.append({"role": "user", "content": question_text})

        try:
            started_at = time.perf_counter()
            
            # Extract chat history (excluding the very last user message we just appended)
            history = [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages[:-1]
            ]
            
            response = ask_question(question_text, chat_history=history)
            roundtrip = time.perf_counter() - started_at

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response.get("answer", "No answer returned."),
                    "sources": response.get("sources", []),
                    "latency": response.get("latency", roundtrip),
                }
            )

        except requests.RequestException as error:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"Could not connect to the RAG API: {error}",
                    "sources": [],
                    "latency": None,
                }
            )

        except Exception as error:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"Question failed: {error}",
                    "sources": [],
                    "latency": None,
                }
            )

        st.rerun()


# ============================================================
# Footer
# ============================================================

render(
    """
    <div class="site-footer">
        TubeRAG
        · FastAPI
        · FAISS
        · Groq
        · Langfuse
    </div>
    """
)
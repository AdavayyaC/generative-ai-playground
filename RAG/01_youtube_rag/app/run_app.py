import html
import re
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
    page_title="Video Intelligence Desk",
    page_icon="◧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Design System
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700'
        '&family=Work+Sans:wght@400;500;600'
        '&family=IBM+Plex+Mono:wght@400;500;600&display=swap'
    );

    :root {
        --bg-void: #0c1210;
        --bg-panel: #131b18;
        --bg-raised: #182420;
        --bg-inset: #0f1613;

        --border: #263029;
        --border-strong: #3a4a41;

        --text-primary: #eef1ea;
        --text-secondary: #93a099;
        --text-muted: #5c6961;

        --accent: #c9a227;
        --accent-strong: #e6bd3a;
        --accent-soft: rgba(201, 162, 39, 0.14);

        --signal: #4a8577;
        --signal-soft: rgba(74, 133, 119, 0.16);

        --recording: #b8453a;

        --radius-lg: 14px;
        --radius-md: 10px;
        --radius-sm: 6px;
    }


    /* ========================================================
       Global
       ======================================================== */

    html,
    body,
    [class*="css"] {
        font-family: "Work Sans", sans-serif;
    }

    .stApp {
        background: var(--bg-void);
        color: var(--text-primary);
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    ::selection {
        background: var(--accent-soft);
        color: var(--text-primary);
    }

    *:focus-visible {
        outline: 2px solid var(--accent) !important;
        outline-offset: 2px;
    }


    /* ========================================================
       Sidebar
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: var(--bg-panel);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem;
    }


    /* ========================================================
       Typography
       ======================================================== */

    h1,
    h2,
    h3 {
        font-family: "Oswald", sans-serif !important;
        color: var(--text-primary) !important;
    }

    h3 {
        font-size: 1.05rem !important;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }


    /* ========================================================
       Sprocket rail
       ======================================================== */

    .sprocket-rail {
        height: 10px;
        width: 100%;
        background-image: radial-gradient(
            circle,
            var(--bg-void) 2.4px,
            transparent 2.6px
        );
        background-size: 18px 10px;
        background-position: 6px center;
        background-color: var(--bg-inset);
        border-radius: 3px;
    }


    /* ========================================================
       Hero
       ======================================================== */

    .chyron {
        border-top: 2px solid var(--accent);
        border-bottom: 1px solid var(--border-strong);
        padding: 1.15rem 0 1.3rem;
        margin-bottom: 1.75rem;
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
        background: var(--recording);
        box-shadow: 0 0 0 3px rgba(184, 69, 58, 0.18);
    }

    .chyron-title {
        font-family: "Oswald", sans-serif;
        font-weight: 700;
        font-size: 2.6rem;
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
        margin-top: 0.55rem;

        color: var(--text-secondary);
        font-size: 0.98rem;
        line-height: 1.6;
    }


    /* ========================================================
       Panels
       ======================================================== */

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


    /* ========================================================
       Sidebar cartridge
       ======================================================== */

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


    /* ========================================================
       Answer
       ======================================================== */

    .caption-card {
        margin: 0.6rem 0 1.4rem;

        background: var(--bg-panel);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: var(--radius-lg);
        overflow: hidden;
    }

    .caption-head {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 0.85rem 1.4rem 0;
    }

    .caption-tag {
        color: var(--accent);

        font-family: "IBM Plex Mono", monospace;
        font-size: 0.7rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .caption-body {
        padding: 0.65rem 1.4rem 1.4rem;

        color: var(--text-primary);
        font-size: 1.06rem;
        line-height: 1.8;
        white-space: pre-wrap;
    }


    /* ========================================================
       Retrieved source frames
       ======================================================== */

    .frame-card {
        margin-bottom: 0.7rem;
        overflow: hidden;

        background: var(--bg-inset);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);

        transition:
            border-color 0.15s ease,
            transform 0.15s ease;
    }

    .frame-card:hover {
        border-color: var(--accent);
        transform: translateY(-1px);
    }

    .frame-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 0.7rem 1rem 0.4rem;
    }

    .frame-number {
        color: var(--accent);

        font-family: "IBM Plex Mono", monospace;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .frame-code {
        color: var(--text-muted);

        font-family: "IBM Plex Mono", monospace;
        font-size: 0.72rem;
        letter-spacing: 1px;
    }

    .frame-text {
        padding: 0.3rem 1rem 1rem;

        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }


    /* ========================================================
       Inputs
       ======================================================== */

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

    .stTextInput input,
    .stTextArea textarea {
        color: var(--text-primary) !important;

        font-family: "IBM Plex Mono", monospace !important;
        font-size: 0.9rem !important;
    }


    /* ========================================================
       Buttons
       ======================================================== */

    div.stButton > button {
        min-height: 44px;

        background: var(--bg-raised);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-sm);

        color: var(--text-primary);

        font-family: "Work Sans", sans-serif;
        font-size: 0.9rem;
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


    /* ========================================================
       Metrics
       ======================================================== */

    div[data-testid="stMetric"] {
        padding: 0.75rem 0.9rem;

        background: var(--bg-inset);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;

        font-family: "IBM Plex Mono", monospace !important;
        font-size: 0.68rem !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: var(--accent) !important;

        font-family: "Oswald", sans-serif !important;
        font-size: 1.7rem !important;
    }


    /* ========================================================
       Alerts
       ======================================================== */

    div[data-testid="stAlert"] {
        background: var(--bg-raised);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-md);
    }


    /* ========================================================
       Expanders
       ======================================================== */

    details {
        background: transparent !important;
        border: none !important;
    }

    summary {
        color: var(--text-secondary) !important;

        font-family: "IBM Plex Mono", monospace !important;
        font-size: 0.8rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }


    /* ========================================================
       Footer
       ======================================================== */

    .site-footer {
        padding-top: 2.5rem;

        color: var(--text-muted);

        font-family: "IBM Plex Mono", monospace;
        font-size: 0.72rem;
        letter-spacing: 1.5px;
        text-align: center;
        text-transform: uppercase;
    }


    /* ========================================================
       Streamlit branding
       ======================================================== */

    #MainMenu,
    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

DEFAULT_STATE = {
    "video_url": None,
    "chunks": None,
    "ingestion_time": None,
    "answer": None,
    "sources": [],
    "backend_latency": None,
}


def initialize_state() -> None:
    """Initialize application state once per Streamlit session."""

    for key, default in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = default


initialize_state()


# ============================================================
# API Layer
# ============================================================

def check_backend_health() -> bool:
    """Return True when the FastAPI backend is reachable."""

    try:
        response = requests.get(
            HEALTH_ENDPOINT,
            timeout=HEALTH_TIMEOUT,
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def ingest_video(url: str) -> Dict[str, Any]:
    """Send a YouTube URL to the ingestion endpoint."""

    response = requests.post(
        VIDEO_ENDPOINT,
        json={"url": url},
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


def ask_question(question: str) -> Dict[str, Any]:
    """Send a question to the RAG endpoint."""

    response = requests.post(
        ASK_ENDPOINT,
        json={"question": question},
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# Data Helpers
# ============================================================

def parse_chunk_count(message: str) -> Optional[int]:
    """Extract the chunk count from an ingestion response."""

    if not message:
        return None

    match = re.search(
        r"Created\s+(\d+)\s+chunks",
        message,
        re.IGNORECASE,
    )

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


def reset_answer() -> None:
    """Clear the current answer and retrieved context."""

    st.session_state.answer = None
    st.session_state.sources = []
    st.session_state.backend_latency = None


# ============================================================
# Hero
# ============================================================

st.markdown(
    """
    <div class="chyron">

        <div class="chyron-eyebrow">
            <span class="chyron-dot"></span>
            LIVE KNOWLEDGE BASE
        </div>

        <div class="chyron-title">
            Video <span>Intelligence</span> Desk
        </div>

        <div class="chyron-subtitle">
            Feed in a YouTube transcript, roll it into a searchable
            index, and pull grounded answers directly from the source
            footage — timecoded, cited, and without guesswork.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="reel-tag">REEL LOADER</div>

        <div class="reel-heading">
            Load a video
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Paste a YouTube URL to build the knowledge base."
    )

    video_url_input = st.text_input(
        "YouTube URL",
        placeholder="https://youtube.com/watch?v=...",
        label_visibility="collapsed",
    )

    process_video = st.button(
        "Process Video",
        type="primary",
        use_container_width=True,
    )

    st.markdown(
        "<div class='sprocket-rail'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div
            class="panel-label"
            style="margin-top:1.1rem;"
        >
            On the reel now
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Active video
    # --------------------------------------------------------

    if st.session_state.video_url:

        current_url = safe_text(
            st.session_state.video_url
        )

        st.markdown(
            f"""
            <div class="cartridge">

                <div class="sprocket-rail"></div>

                <div class="cartridge-body">

                    <div class="cartridge-label">
                        Active source
                    </div>

                    <div class="cartridge-url">
                        {current_url}
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        metric_col_1, metric_col_2 = st.columns(2)

        with metric_col_1:
            st.metric(
                "Chunks",
                st.session_state.chunks
                if st.session_state.chunks is not None
                else "—",
            )

        with metric_col_2:
            st.metric(
                "Indexed in",
                format_timecode(
                    st.session_state.ingestion_time
                ),
            )

    else:

        st.markdown(
            """
            <div class="empty-slate">
                No footage loaded yet.<br><br>
                Process a video to start the reel
                and unlock questions.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-footnote">
            ONE ACTIVE VIDEO AT A TIME<br>
            FASTAPI · FAISS · GROQ
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Process Video
# ============================================================

if process_video:

    url = video_url_input.strip()

    if not url:

        st.error(
            "Please paste a YouTube URL first."
        )

    elif not check_backend_health():

        st.error(
            "The RAG API is unreachable. "
            "Start the FastAPI server at "
            f"{BASE_URL}."
        )

    else:

        with st.spinner(
            "Rolling the transcript into the index..."
        ):

            try:

                started_at = time.perf_counter()

                result = ingest_video(url)

                elapsed = (
                    time.perf_counter()
                    - started_at
                )

                chunks = parse_chunk_count(
                    result.get("message", "")
                )

                st.session_state.video_url = (
                    result.get("url") or url
                )

                st.session_state.chunks = chunks

                st.session_state.ingestion_time = elapsed

                reset_answer()

                st.success(
                    "Video processed successfully."
                )

            except requests.RequestException as error:

                st.error(
                    "Could not connect to the RAG API: "
                    f"{error}"
                )

            except Exception as error:

                st.error(
                    f"Video processing failed: {error}"
                )


# ============================================================
# Question Panel
# ============================================================

st.markdown(
    """
    <div class="panel">

        <div class="sprocket-rail"></div>

        <div class="panel-body">

            <div class="panel-label">
                Console
            </div>

            <div class="panel-title">
                Ask the footage
            </div>

            <div class="panel-description">
                Ask factual questions, request explanations,
                or summarize the video in your own words.
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


question = st.text_area(
    "Question",
    placeholder=(
        "What did the speaker say about AI?\n"
        "Summarize the video in 100 words."
    ),
    height=110,
    label_visibility="collapsed",
)

ask_button = st.button(
    "Ask Question  →",
    type="primary",
)


# ============================================================
# Ask Question
# ============================================================

if ask_button:

    question_text = question.strip()

    if not st.session_state.video_url:

        st.warning(
            "Please process a YouTube video "
            "before asking a question."
        )

    elif not question_text:

        st.warning(
            "Please enter a question."
        )

    elif not check_backend_health():

        st.error(
            "The RAG API is unreachable. "
            f"Start the FastAPI server at {BASE_URL}."
        )

    else:

        with st.spinner(
            "Scanning the reel for an answer..."
        ):

            try:

                started_at = time.perf_counter()

                response = ask_question(
                    question_text
                )

                roundtrip = (
                    time.perf_counter()
                    - started_at
                )

                st.session_state.answer = (
                    response.get(
                        "answer",
                        "No answer returned.",
                    )
                )

                st.session_state.sources = (
                    response.get(
                        "sources",
                        [],
                    )
                )

                st.session_state.backend_latency = (
                    response.get(
                        "latency",
                        roundtrip,
                    )
                )

            except requests.RequestException as error:

                st.error(
                    "Could not connect to the RAG API: "
                    f"{error}"
                )

            except Exception as error:

                st.error(
                    f"Question failed: {error}"
                )


# ============================================================
# Answer
# ============================================================

if st.session_state.answer:

    st.markdown("### Answer")

    answer_html = safe_text(
        st.session_state.answer
    )

    st.markdown(
        f"""
        <div class="caption-card">

            <div class="caption-head">

                <span class="caption-tag">
                    Transcript Analysis
                </span>

                <span class="caption-tag">
                    CC
                </span>

            </div>

            <div class="caption-body">
                {answer_html}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # Performance Metrics
    # ========================================================

    st.markdown("### Performance")

    latency = st.session_state.backend_latency

    metric_1, metric_2, metric_3 = st.columns(3)

    with metric_1:

        st.metric(
            "RAG Latency",
            (
                f"{latency:.2f}s"
                if latency is not None
                else "—"
            ),
        )

    with metric_2:

        st.metric(
            "Sources",
            len(st.session_state.sources),
        )

    with metric_3:

        st.metric(
            "Chunks",
            (
                st.session_state.chunks
                if st.session_state.chunks is not None
                else "—"
            ),
        )


    # ========================================================
    # Retrieved Sources
    # ========================================================

    st.markdown("### Retrieved Context")

    sources: List[Dict[str, Any]] = (
        st.session_state.sources
    )

    if sources:

        for index, source in enumerate(
            sources,
            start=1,
        ):

            content = source.get(
                "content",
                "",
            )

            metadata = source.get(
                "metadata",
                {},
            )

            with st.expander(
                f"Frame {index:02d}",
                expanded=False,
            ):

                safe_content = safe_text(
                    content
                )

                st.markdown(
                    f"""
                    <div class="frame-card">

                        <div class="frame-meta">

                            <span class="frame-number">
                                FRAME {index:02d}
                            </span>

                            <span class="frame-code">
                                RETRIEVED · CHUNK {index}
                            </span>

                        </div>

                        <div class="frame-text">
                            {safe_content}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if metadata:

                    st.caption(
                        "Metadata"
                    )

                    st.json(metadata)

    else:

        st.info(
            "No retrieved sources were returned."
        )


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div class="site-footer">
        Video Intelligence Desk
        · FastAPI
        · FAISS
        · Groq
        · Langfuse
    </div>
    """,
    unsafe_allow_html=True,
)
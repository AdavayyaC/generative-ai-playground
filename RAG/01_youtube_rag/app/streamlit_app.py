import re
import time
import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# API helpers
# ============================================================

def ingest_video(url: str):
    import re
    import time
    import requests
    import streamlit as st

    BASE_URL = "http://127.0.0.1:8000"


    def ingest_video(url: str):
        resp = requests.post(f"{BASE_URL}/videos", json={"url": url}, timeout=300)
        resp.raise_for_status()
        return resp.json()


    def ask_question(question: str):
        resp = requests.post(f"{BASE_URL}/ask", json={"question": question}, timeout=120)
        resp.raise_for_status()
        return resp.json()


    def parse_chunk_count(message: str):
        m = re.search(r"Created (\d+) chunks", message)
        if m:
            return int(m.group(1))
        return None


    def check_health():
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            return False
        return False


    def main():
        st.set_page_config(
            page_title="YouTube RAG Demo",
            page_icon="🎞️",
            layout="wide",
        )

        # Sidebar
        with st.sidebar:
            st.title("YouTube RAG")
            st.write("A clean demo UI that calls the existing FastAPI backend.")
            st.markdown("---")
            st.write("Backend:")
            healthy = check_health()
            if healthy:
                st.success("API: healthy")
            else:
                st.error("API: unreachable — start the FastAPI server at http://127.0.0.1:8000")

            st.markdown("---")
            st.write("Example URLs")
            if st.button("Use example: TED talk"):
                st.session_state['sample_url'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        # Header
        st.markdown("# YouTube RAG — Demo")
        st.markdown("A simple, polished demo — ingest a YouTube transcript and query it.")

        # Input area
        left, right = st.columns([3, 1])
        with left:
            url = st.text_input("YouTube URL", value=st.session_state.get('sample_url', ''), placeholder="https://www.youtube.com/watch?v=...")
        with right:
            ingest_btn = st.button("Ingest Video", key="ingest", use_container_width=True)

        # Status and metrics
        status_col1, status_col2, status_col3 = st.columns(3)
        ingest_status = st.empty()

        if ingest_btn:
            if not url:
                ingest_status.error("Please enter a YouTube URL.")
            else:
                if not healthy:
                    ingest_status.error("Backend unreachable. Start FastAPI at http://127.0.0.1:8000")
                else:
                    with st.spinner("Running ingestion — this can take a minute or two..."):
                        try:
                            t0 = time.perf_counter()
                            result = ingest_video(url)
                            t1 = time.perf_counter()
                            rt = t1 - t0

                            st.session_state['last_ingest'] = result

                            ingest_status.success("Ingestion completed")

                            count = parse_chunk_count(result.get('message', ''))

                            status_col1.metric("Status", result.get('status', ''))
                            status_col2.metric("Video URL", result.get('url', ''))
                            status_col3.metric("Chunks", count if count is not None else "—")

                            st.markdown(f"*Ingestion roundtrip: {rt:.2f}s*")
                        except Exception as e:
                            ingest_status.error(f"Ingestion failed: {e}")

        # Ingestion result preview
        if st.session_state.get('last_ingest'):
            with st.expander("Last ingestion result"):
                st.json(st.session_state['last_ingest'])

        st.markdown("---")

        # Ask section
        st.header("Ask a question")
        qcol, qbtncol = st.columns([4, 1])
        with qcol:
            question = st.text_input("Your question", key="question_input")
        with qbtncol:
            ask_btn = st.button("Ask", key="ask", use_container_width=True)

        if ask_btn:
            if not question:
                st.error("Please type a question first.")
            else:
                if not healthy:
                    st.error("Backend unreachable. Start FastAPI at http://127.0.0.1:8000")
                else:
                    with st.spinner("Querying the RAG backend..."):
                        try:
                            t0 = time.perf_counter()
                            resp = ask_question(question)
                            t1 = time.perf_counter()
                            rt = t1 - t0

                            st.session_state['last_ask'] = resp

                            answer = resp.get('answer', '')
                            backend_latency = resp.get('latency')
                            sources = resp.get('sources', [])

                            st.subheader("Answer")
                            st.success(answer)

                            m1, m2 = st.columns(2)
                            m1.metric("Backend latency (s)", f"{backend_latency:.3f}" if backend_latency is not None else "—")
                            m2.metric("Roundtrip (s)", f"{rt:.3f}")

                            if sources:
                                st.markdown("**Retrieved sources**")
                                for i, s in enumerate(sources, start=1):
                                    title = s.get('metadata', {}).get('source', f"source-{i}")
                                    with st.expander(f"{i}. {title}"):
                                        st.write(s.get('content', ''))
                                        st.json(s.get('metadata', {}))
                            else:
                                st.info("No sources returned by the backend.")

                        except Exception as e:
                            st.error(f"Ask failed: {e}")


    if __name__ == '__main__':
        main()
        border: 1px solid #282d36;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }

    .source-number {
        color: #ff6b6b;
        font-weight: 700;
        font-size: 0.85rem;
    }

    .source-text {
        color: #b8bec9;
        font-size: 0.88rem;
        line-height: 1.55;
        margin-top: 0.45rem;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8rem;
        padding-top: 2rem;
    }

    /* ---------- Buttons ---------- */

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    /* ---------- Inputs ---------- */

    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    /* ---------- Hide Streamlit branding ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session state
# ============================================================

if "video_url" not in st.session_state:
    st.session_state.video_url = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "ingestion_time" not in st.session_state:
    st.session_state.ingestion_time = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "sources" not in st.session_state:
    st.session_state.sources = []

if "backend_latency" not in st.session_state:
    st.session_state.backend_latency = None


# ============================================================
# Hero
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            YouTube <span>RAG</span>
        </div>

        <div class="hero-subtitle">
            Turn any YouTube video into a searchable knowledge base.
            Ingest the transcript, then ask questions and get
            grounded answers from the video.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar — ingestion
# ============================================================

with st.sidebar:

    st.markdown("## ▶️ Video")

    st.caption(
        "Paste a YouTube URL to create the knowledge base."
    )

    url = st.text_input(
        "YouTube URL",
        placeholder="https://youtube.com/watch?v=...",
        label_visibility="collapsed",
    )

    ingest_btn = st.button(
        "Process Video",
        type="primary",
        use_container_width=True,
    )

    st.markdown("---")

    st.markdown("### Current knowledge base")

    if st.session_state.video_url:

        st.markdown(
            f"""
            <div class="active-video">
                <div class="active-label">
                    Active Video
                </div>

                <div class="active-url">
                    {st.session_state.video_url}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Chunks",
                st.session_state.chunks
                if st.session_state.chunks is not None
                else "—",
            )

        with col2:
            st.metric(
                "Status",
                "Ready",
            )

    else:

        st.info(
            "No video loaded yet.\n\n"
            "Process a YouTube video to start asking questions."
        )

    st.markdown("---")

    st.caption(
        "One active video at a time • "
        "FastAPI + FAISS + Groq"
    )


# ============================================================
# Video ingestion
# ============================================================

if ingest_btn:

    if not url.strip():

        st.error(
            "Please paste a YouTube URL first."
        )

    else:

        with st.spinner(
            "Processing video transcript..."
        ):

            try:

                start = time.perf_counter()

                result = ingest_video(url.strip())

                elapsed = time.perf_counter() - start

                chunks = parse_chunk_count(
                    result.get("message", "")
                )

                # Update active knowledge base
                st.session_state.video_url = result.get(
                    "url",
                    url,
                )

                st.session_state.chunks = chunks

                st.session_state.ingestion_time = elapsed

                # Clear previous answer because the knowledge
                # base has changed.
                st.session_state.answer = None
                st.session_state.sources = []
                st.session_state.backend_latency = None

                st.success(
                    "Video processed successfully."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to the RAG API: {e}"
                )

            except Exception as e:

                st.error(
                    f"Video processing failed: {e}"
                )


# ============================================================
# Main question area
# ============================================================

st.markdown(
    """
    <div class="card">
        <div class="card-title">
            Ask your video
        </div>

        <div class="card-description">
            Ask factual questions, request explanations,
            or summarize the content.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


question = st.text_area(
    "Question",
    placeholder=(
        "e.g. What did the speaker say about AI?\n"
        "e.g. Summarize the video in 100 words."
    ),
    height=110,
    label_visibility="collapsed",
)

ask_btn = st.button(
    "Ask Question  →",
    type="primary",
)


# ============================================================
# Ask API
# ============================================================

if ask_btn:

    if not st.session_state.video_url:

        st.warning(
            "Please process a YouTube video before asking a question."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Searching the video and generating an answer..."
        ):

            try:

                start = time.perf_counter()

                response = ask_question(
                    question.strip()
                )

                roundtrip = time.perf_counter() - start

                st.session_state.answer = response.get(
                    "answer",
                    "No answer returned.",
                )

                st.session_state.sources = response.get(
                    "sources",
                    [],
                )

                st.session_state.backend_latency = response.get(
                    "latency"
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to the RAG API: {e}"
                )

            except Exception as e:

                st.error(
                    f"Question failed: {e}"
                )


# ============================================================
# Answer
# ============================================================

if st.session_state.answer:

    st.markdown("### Answer")

    st.markdown(
        f"""
        <div class="answer-card">
            <div class="answer-text">
                {st.session_state.answer}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # Metrics
    # ========================================================

    st.markdown("### Performance")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:

        latency = st.session_state.backend_latency

        st.metric(
            "RAG Latency",
            f"{latency:.2f}s"
            if latency is not None
            else "—",
        )

    with metric2:

        st.metric(
            "Sources",
            len(st.session_state.sources),
        )

    with metric3:

        st.metric(
            "Chunks",
            st.session_state.chunks
            if st.session_state.chunks is not None
            else "—",
        )


    # ========================================================
    # Sources
    # ========================================================

    st.markdown("### Retrieved context")

    sources = st.session_state.sources

    if sources:

        for i, source in enumerate(
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
                f"Source {i}",
                expanded=False,
            ):

                st.markdown(
                    f"""
                    <div class="source-card">

                        <div class="source-number">
                            RETRIEVED CHUNK {i}
                        </div>

                        <div class="source-text">
                            {content}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if metadata:

                    st.caption("Metadata")

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
    <div class="footer">
        YouTube RAG • FastAPI • FAISS • Groq • Langfuse
    </div>
    """,
    unsafe_allow_html=True,
)
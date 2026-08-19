"""Streamlit UI for the AI writing assistant."""

from __future__ import annotations

import json
from typing import Any

import streamlit as st

from . import config
from .model import create_model, has_groq_key
from .parsing import parse_json_response, validate_brief
from .pipeline import demo_pipeline, demo_polish, polish_draft, run_pipeline


def render_quality_panel(quality: dict[str, Any]) -> None:
    st.subheader("Quality check")
    badge = "\u2705 Approved" if quality.get("approved") else "\u26a0\ufe0f Needs revision"
    st.metric("Overall score", f"{quality.get('overall_score', 0)}/10", badge)
    cols = st.columns(4)
    for col, key in zip(cols, ["clarity", "audience_fit", "brief_coverage", "voice_consistency"]):
        col.metric(key.replace("_", " ").title(), quality.get(key, 0))
    feedback = quality.get("feedback", [])
    if feedback:
        st.caption("Reviewer feedback")
        for item in feedback:
            st.write(f"- {item}")


def render_draft(draft: dict[str, Any], format_: str) -> None:
    """Render the draft in a way that actually looks like its format instead
    of one flat paragraph block for everything."""
    content = draft.get("content", "")
    if format_ == "email":
        lines = content.split("\n")
        if lines and lines[0].lower().startswith("subject:"):
            st.markdown(f"**{lines[0]}**")
            st.markdown("\n".join(lines[1:]))
        else:
            st.markdown(content)
    else:
        # blog / report use markdown '##' headings already requested in the
        # prompt; social is short enough that plain markdown is fine too.
        st.markdown(content)


def copy_ready_text(draft: dict[str, Any]) -> str:
    """Build clean plain text containing only the title and written content."""
    title = str(draft.get("title", "")).strip()
    content = str(draft.get("content", "")).strip()
    return "\n\n".join(part for part in (title, content) if part)


def _render_generate_tab(demo_mode: bool, voice: str, length: str, temperature: float, max_attempts: int) -> None:
    user_input = st.text_area(
        "Describe what you want to write",
        placeholder="A practical blog post helping new managers run better one-on-ones",
        height=140,
        key="generate_input",
    )

    if st.button("Generate draft", type="primary", use_container_width=True, key="generate_btn"):
        if not user_input.strip():
            st.warning("Describe a topic, audience, or desired outcome first.")
        else:
            try:
                if demo_mode:
                    with st.status("Running demo pipeline...", expanded=True) as status:
                        st.write("Extracting content brief from your description...")
                        brief = validate_brief(parse_json_response(json.dumps({
                            "topic": user_input.strip()[:80] or "your topic",
                            "audience": "your target audience",
                            "tone": "professional",
                            "format": "blog",
                            "key_points": [
                                "Start with the reader's goal",
                                "Keep each step concrete",
                                "Close with a clear next action",
                            ],
                        })))
                        st.write("Writing the draft...")
                        draft, quality = demo_pipeline(brief, config.LENGTH_OPTIONS[length])
                        history = [{"attempt": 1, "draft": draft, "quality": quality}]
                        status.update(label="Demo pipeline complete", state="complete")
                else:
                    with st.status("Running pipeline...", expanded=True) as status:
                        def on_step(msg: str) -> None:
                            st.write(msg)

                        model = create_model(temperature)
                        brief, draft, quality, history = run_pipeline(
                            model, user_input, config.LENGTH_OPTIONS[length], max_attempts, on_step, voice
                        )
                        status.update(
                            label="Pipeline complete" if quality["approved"] else "Pipeline complete (not approved)",
                            state="complete",
                        )

                st.session_state.result = {
                    "brief": brief,
                    "draft": draft,
                    "quality": quality,
                    "history": history,
                    "mode": "demo" if demo_mode else "live",
                }
            except Exception as exc:
                st.error(f"Generation failed: {exc}")

    result = st.session_state.get("result")
    if result:
        brief, draft, quality = result["brief"], result["draft"], result["quality"]
        history = result.get("history", [])

        left, right = st.columns([2, 1])
        with left:
            st.subheader(draft.get("title", "Untitled draft"))
            render_draft(draft, brief.get("format", "blog"))
            st.caption(f"{draft.get('word_count', 0)} words \u00b7 {result.get('mode', 'live')} mode")
            copy_text = copy_ready_text(draft)
            st.text_area("Copy-ready output", copy_text, height=260)
            st.download_button(
                "Download text",
                copy_text,
                "writing-assistant-draft.txt",
                "text/plain",
            )
            st.download_button(
                "Download JSON",
                json.dumps(result, indent=2),
                "writing-assistant-result.json",
                "application/json",
            )
            if len(history) > 1:
                with st.expander(f"Revision history ({len(history)} attempts)"):
                    for entry in history:
                        st.markdown(f"**Attempt {entry['attempt']}** \u2014 score {entry['quality'].get('overall_score', 0)}/10")
                        st.write(entry["draft"].get("content", ""))
                        st.divider()
        with right:
            render_quality_panel(quality)
            with st.expander("Extracted brief"):
                st.json(brief)


def _render_polish_tab(demo_mode: bool, voice: str, temperature: float) -> None:
    st.caption(
        "Paste something you've already written \u2014 a cold email, a CV summary, "
        "an outreach note \u2014 and get it back in fluent, natural English. "
        "Nothing is invented; only your own wording is cleaned up."
    )
    polish_format = st.selectbox(
        "This is a...", config.FORMAT_OPTIONS, index=config.FORMAT_OPTIONS.index("email"), key="polish_format"
    )
    original_text = st.text_area(
        "Your draft",
        placeholder="Hi, I am writing to you because I saw job posting for SDE role in your company and I have relevant skills so please consider my application...",
        height=180,
        key="polish_input",
    )

    if st.button("Polish my draft", type="primary", use_container_width=True, key="polish_btn"):
        if not original_text.strip():
            st.warning("Paste the text you want polished first.")
        else:
            try:
                if demo_mode:
                    with st.spinner("Running demo polish..."):
                        polished = demo_polish(original_text, polish_format)
                else:
                    with st.spinner("Polishing your draft..."):
                        model = create_model(temperature)
                        polished = polish_draft(model, original_text, polish_format, voice)
                st.session_state.polish_result = {
                    "original": original_text,
                    "polished": polished,
                    "format": polish_format,
                    "mode": "demo" if demo_mode else "live",
                }
            except Exception as exc:
                st.error(f"Polishing failed: {exc}")

    polish_result = st.session_state.get("polish_result")
    if polish_result:
        polished = polish_result["polished"]
        before, after = st.columns(2)
        with before:
            st.subheader("Before")
            st.text(polish_result["original"])
        with after:
            st.subheader("After")
            render_draft(polished, polish_result["format"])
            st.caption(f"{polished.get('word_count', 0)} words \u00b7 {polish_result.get('mode', 'live')} mode")
            polished_text = copy_ready_text(polished)
            st.text_area("Copy-ready polished output", polished_text, height=220)

        changes = polished.get("changes_summary", [])
        if changes:
            st.caption("What changed")
            for item in changes:
                st.write(f"- {item}")

        st.download_button(
            "Download polished text",
            polished_text,
            "polished-draft.txt",
            "text/plain",
        )


def main() -> None:
    st.set_page_config(page_title="AI Writing Assistant", page_icon="\u270d\ufe0f", layout="wide")
    st.title("\u270d\ufe0f AI Writing Assistant")
    st.caption("Brief \u2192 draft \u2192 quality check, with format-aware structure and a voice you control.")

    with st.sidebar:
        st.header("Writing controls")
        voice = st.selectbox(
            "Voice", list(config.VOICE_OPTIONS), index=list(config.VOICE_OPTIONS).index(config.DEFAULT_VOICE)
        )
        length = st.select_slider("Length", options=list(config.LENGTH_OPTIONS), value="Medium")
        temperature = st.slider("Creativity", 0.0, 1.0, 0.3, 0.1)
        max_attempts = st.slider("Max revision attempts", 1, 3, config.DEFAULT_MAX_ATTEMPTS)

        st.divider()
        demo_mode = st.checkbox(
            "Demo mode (no API calls)",
            value=not has_groq_key(),
            help="Runs a deterministic offline pipeline instead of calling Groq. "
                 "Useful with no API key, or to sanity-check the app's plumbing.",
        )
        if not has_groq_key() and not demo_mode:
            st.warning("No GROQ_API_KEY found in the environment. Set one in .env, or keep Demo mode on.")

    tab_generate, tab_polish = st.tabs(["\u2728 Generate new", "\U0001fa79 Polish my draft"])
    with tab_generate:
        _render_generate_tab(demo_mode, voice, length, temperature, max_attempts)
    with tab_polish:
        _render_polish_tab(demo_mode, voice, temperature)
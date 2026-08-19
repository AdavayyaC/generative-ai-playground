"""Streamlit AI writing assistant built around a prompt-engineered pipeline."""

from __future__ import annotations

import json
import re
from typing import Any

import streamlit as st
from dotenv import load_dotenv


SYSTEM_PROMPT = """You are a professional content strategist and copywriter.

You write clear, compelling content tailored precisely to the target audience.
You never use filler phrases, passive voice, or unnecessary adjectives.
You always follow the requested format exactly.

Output format: Always return valid JSON matching the schema provided. Do not wrap
JSON in markdown fences and do not add commentary outside the JSON object.

Few-shot examples of the target style:
1. {"title":"A calmer way to plan your week","content":"Choose three priorities before opening your inbox. Give each one a clear finish line, then protect a short block of focused time. A smaller plan is easier to start and more satisfying to finish.","word_count":42}
2. {"title":"Your report is ready","content":"The launch reached 94% of its adoption goal in the first month. Support requests were concentrated in setup, so the next iteration will add an onboarding checklist and a guided first run.","word_count":35}
3. {"title":"Subject: A practical next step","content":"Hi Maya,\n\nI have attached the revised proposal. The new timeline keeps the research phase focused and gives the team a clear review point on Friday.\n\nBest,\nAlex","word_count":35}
"""

BRIEF_PROMPT = """Extract a content brief from the user's description.
Return exactly this JSON schema:
{{
  "topic": "string",
  "audience": "string",
  "tone": "professional|casual|technical|inspirational",
  "format": "blog|email|report|social",
  "key_points": ["string"]
}}

Infer sensible defaults when details are missing. Keep key_points specific and
useful, with 3 to 5 items.

User description: {user_input}
"""

CONTENT_PROMPT = """Write a {format} about {topic} for {audience}.

Key points to cover:
{key_points}

Tone: {tone}
Length guidance: {length_guidance}
Brand voice: clear, direct, useful, and human. Use active voice and no filler.

Return exactly this JSON object:
{{"title": "string", "content": "string", "word_count": number}}
"""

QUALITY_PROMPT = """Evaluate the draft against its brief. Return only valid JSON:
{{
  "overall_score": number,
  "clarity": number,
  "audience_fit": number,
  "brief_coverage": number,
  "voice_consistency": number,
  "feedback": ["string"],
  "approved": boolean
}}

Scores must be integers from 1 to 10. Approve only when overall_score is at
least 7. Be specific and concise in feedback.

Brief: {brief}
Draft: {draft}
"""

TONE_OPTIONS = ["professional", "casual", "technical", "inspirational"]
FORMAT_OPTIONS = ["blog", "email", "report", "social"]
LENGTH_OPTIONS = {
    "Short": "150 to 250 words",
    "Medium": "350 to 500 words",
    "Long": "700 to 900 words",
}
GROQ_MODEL = "openai/gpt-oss-120b"


def parse_json_response(response: Any) -> dict[str, Any]:
    """Parse a model response while tolerating accidental markdown fences."""
    raw = response.content if hasattr(response, "content") else str(response)
    cleaned = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw.strip())
    parsed = json.loads(cleaned)
    if not isinstance(parsed, dict):
        raise ValueError("The model returned JSON, but not a JSON object.")
    return parsed


def validate_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Normalize and validate the contract between the first two stages."""
    required = ["topic", "audience", "tone", "format", "key_points"]
    missing = [field for field in required if not brief.get(field)]
    if missing:
        raise ValueError(f"Brief is missing: {', '.join(missing)}")
    if brief["tone"] not in TONE_OPTIONS or brief["format"] not in FORMAT_OPTIONS:
        raise ValueError("Brief contains an unsupported tone or format.")
    if not isinstance(brief["key_points"], list):
        raise ValueError("Brief key_points must be a list.")
    return brief


def demo_pipeline(brief: dict[str, Any], length_guidance: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a predictable result for local exploration without an API key."""
    title = f"{brief['topic'].title()}: a practical guide"
    points = ". ".join(point.rstrip(".") for point in brief["key_points"])
    content = f"{title}\n\nFor {brief['audience']}, the most useful way to approach {brief['topic']} is to keep the goal clear and the next action small. {points}. Start with one concrete step, review what you learn, and improve the process as you go."
    draft = {"title": title, "content": content, "word_count": len(content.split())}
    quality = {"overall_score": 8, "clarity": 8, "audience_fit": 8, "brief_coverage": 8, "voice_consistency": 8, "feedback": [f"Demo draft generated within the requested {length_guidance} guidance."], "approved": True}
    return draft, quality


@st.cache_resource(show_spinner=False)
def create_model(temperature: float) -> Any:
    load_dotenv()
    from langchain_groq import ChatGroq

    return ChatGroq(model=GROQ_MODEL, temperature=temperature)


def run_pipeline(model: Any, user_input: str, length_guidance: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    brief = validate_brief(parse_json_response(model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", BRIEF_PROMPT.format(user_input=user_input)),
    ])))
    draft = parse_json_response(model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", CONTENT_PROMPT.format(format=brief["format"], topic=brief["topic"], audience=brief["audience"], key_points="\n".join(f"- {point}" for point in brief["key_points"]), tone=brief["tone"], length_guidance=length_guidance)),
    ]))
    quality = parse_json_response(model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", QUALITY_PROMPT.format(brief=json.dumps(brief), draft=json.dumps(draft))),
    ]))
    return brief, draft, quality


def main() -> None:
    st.set_page_config(page_title="AI Writing Assistant", page_icon="✍️", layout="wide")
    st.title("AI Writing Assistant")
    st.caption("Turn a rough idea into audience-aware, brand-consistent content.")

    with st.sidebar:
        st.header("Writing controls")
        length = st.select_slider("Length", options=list(LENGTH_OPTIONS), value="Medium")
        temperature = st.slider("Creativity", 0.0, 1.0, 0.3, 0.1)

    user_input = st.text_area("Describe what you want to write", placeholder="A practical blog post helping new managers run better one-on-ones", height=140)
    if st.button("Generate draft", type="primary", use_container_width=True):
        if not user_input.strip():
            st.warning("Describe a topic, audience, or desired outcome first.")
            return
        try:
            with st.spinner("Extracting brief, writing draft, and checking quality..."):
                model = create_model(temperature)
                brief, draft, quality = run_pipeline(model, user_input, LENGTH_OPTIONS[length])
            st.session_state.result = {"brief": brief, "draft": draft, "quality": quality}
        except Exception as exc:
            st.error(f"Generation failed: {exc}")

    result = st.session_state.get("result")
    if result:
        brief, draft, quality = result["brief"], result["draft"], result["quality"]
        left, right = st.columns([2, 1])
        with left:
            st.subheader(draft.get("title", "Untitled draft"))
            st.write(draft.get("content", ""))
            st.download_button("Download JSON", json.dumps(result, indent=2), "writing-assistant-result.json", "application/json")
        with right:
            st.subheader("Quality check")
            st.metric("Overall score", f"{quality.get('overall_score', 0)}/10")
            st.write("Approved" if quality.get("approved") else "Needs revision")
            st.json({key: quality.get(key) for key in ["clarity", "audience_fit", "brief_coverage", "voice_consistency"]})
            st.write(quality.get("feedback", []))
            with st.expander("Extracted brief"):
                st.json(brief)


if __name__ == "__main__":
    main()
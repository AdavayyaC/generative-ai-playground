"""The prompt-engineered pipeline: brief extraction -> draft generation ->
quality check, with an automatic revision loop, plus a separate "polish my
own draft" mode for cleaning up text the user already wrote themselves.
"""

from __future__ import annotations

import json
from typing import Any

from . import config
from .parsing import (
    parse_delimited_draft,
    parse_delimited_polish,
    parse_json_response,
    validate_brief,
    validate_quality,
)
from .prompts import (
    BRIEF_PROMPT,
    CONTENT_PROMPT,
    CONTENT_REVISION_PROMPT,
    POLISH_PROMPT,
    QUALITY_PROMPT,
    SYSTEM_PROMPT,
)


def extract_brief(model: Any, user_input: str) -> dict[str, Any]:
    return validate_brief(parse_json_response(model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", BRIEF_PROMPT.format(user_input=user_input)),
    ])))


def generate_draft(
    model: Any,
    brief: dict[str, Any],
    length_guidance: str,
    voice: str = config.DEFAULT_VOICE,
) -> dict[str, Any]:
    response = model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", CONTENT_PROMPT.format(
            format=brief["format"],
            topic=brief["topic"],
            audience=brief["audience"],
            key_points="\n".join(f"- {point}" for point in brief["key_points"]),
            tone=brief["tone"],
            length_guidance=length_guidance,
            voice_guidance=config.VOICE_OPTIONS.get(voice, config.VOICE_OPTIONS[config.DEFAULT_VOICE]),
            format_guidance=config.FORMAT_GUIDANCE.get(brief["format"], "Use clear, well-organized prose."),
        )),
    ])
    return parse_delimited_draft(response)


def revise_draft(
    model: Any,
    brief: dict[str, Any],
    previous_draft: dict[str, Any],
    feedback: list[str],
    length_guidance: str,
    voice: str = config.DEFAULT_VOICE,
) -> dict[str, Any]:
    response = model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", CONTENT_REVISION_PROMPT.format(
            format=brief["format"],
            topic=brief["topic"],
            audience=brief["audience"],
            previous_draft=previous_draft.get("content", ""),
            feedback="; ".join(feedback) or "No specific feedback was given; tighten the writing generally.",
            key_points="\n".join(f"- {point}" for point in brief["key_points"]),
            tone=brief["tone"],
            length_guidance=length_guidance,
            voice_guidance=config.VOICE_OPTIONS.get(voice, config.VOICE_OPTIONS[config.DEFAULT_VOICE]),
            format_guidance=config.FORMAT_GUIDANCE.get(brief["format"], "Use clear, well-organized prose."),
        )),
    ])
    return parse_delimited_draft(response)


def polish_draft(
    model: Any,
    original_text: str,
    format_: str,
    voice: str = config.DEFAULT_VOICE,
) -> dict[str, Any]:
    """Rewrite the user's own rough draft (cold email, CV blurb, etc.) into
    fluent, natural English without inventing new content."""
    response = model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", POLISH_PROMPT.format(
            format=format_,
            voice_guidance=config.VOICE_OPTIONS.get(voice, config.VOICE_OPTIONS[config.DEFAULT_VOICE]),
            format_guidance=config.FORMAT_GUIDANCE.get(format_, "Use clear, well-organized prose."),
            original_text=original_text,
        )),
    ])
    return parse_delimited_polish(response)


def check_quality(model: Any, brief: dict[str, Any], draft: dict[str, Any]) -> dict[str, Any]:
    return validate_quality(parse_json_response(model.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", QUALITY_PROMPT.format(brief=json.dumps(brief), draft=json.dumps(draft))),
    ])))


def run_pipeline(
    model: Any,
    user_input: str,
    length_guidance: str,
    max_attempts: int = config.DEFAULT_MAX_ATTEMPTS,
    on_step: Any = None,
    voice: str = config.DEFAULT_VOICE,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    """Run brief extraction, then draft + quality-check, revising the draft
    up to `max_attempts` times if the quality checker doesn't approve it.
    `on_step`, if given, is called with a short status string after each stage.
    """
    if on_step:
        on_step("Extracting content brief from your description...")
    brief = extract_brief(model, user_input)

    history: list[dict[str, Any]] = []
    draft: dict[str, Any] | None = None
    quality: dict[str, Any] | None = None

    for attempt in range(1, max_attempts + 1):
        if on_step:
            verb = "Writing" if attempt == 1 else f"Revising (attempt {attempt}/{max_attempts})"
            on_step(f"{verb} the {brief['format']}...")

        if attempt == 1:
            draft = generate_draft(model, brief, length_guidance, voice)
        else:
            draft = revise_draft(model, brief, draft, quality["feedback"], length_guidance, voice)

        if on_step:
            on_step("Checking quality against the brief...")
        quality = check_quality(model, brief, draft)

        history.append({"attempt": attempt, "draft": draft, "quality": quality})

        if quality["approved"]:
            break

    return brief, draft, quality, history


def demo_pipeline(brief: dict[str, Any], length_guidance: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a predictable result for local exploration without an API key."""
    title = f"{brief['topic'].title()}: a practical guide"
    points = ". ".join(point.rstrip(".") for point in brief["key_points"])
    content = f"{title}\n\nFor {brief['audience']}, the most useful way to approach {brief['topic']} is to keep the goal clear and the next action small. {points}. Start with one concrete step, review what you learn, and improve the process as you go."
    draft = {"title": title, "content": content, "word_count": len(content.split())}
    quality = {"overall_score": 8, "clarity": 8, "audience_fit": 8, "brief_coverage": 8, "voice_consistency": 8, "feedback": [f"Demo draft generated within the requested {length_guidance} guidance."], "approved": True}
    return draft, quality


def demo_polish(original_text: str, format_: str) -> dict[str, Any]:
    """Offline stand-in for polish_draft so Demo mode covers this feature too."""
    tidy = " ".join(original_text.split())
    prefix = "Subject: Following up\n\n" if format_ == "email" else ""
    content = f"{prefix}{tidy}"
    return {
        "title": "Polished draft (demo)",
        "content": content,
        "word_count": len(content.split()),
        "changes_summary": [
            "Demo mode: whitespace normalized only \u2014 connect a live model for real grammar and tone edits."
        ],
    }
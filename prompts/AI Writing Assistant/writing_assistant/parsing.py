"""Response parsing and validation helpers.

`parse_json_response` is used for the short structured outputs (brief,
quality scores). `parse_delimited_draft` / `parse_delimited_polish` are used
for anything containing long free-form prose — see prompts.py for why JSON
is deliberately avoided there.
"""

from __future__ import annotations

import json
import re
from typing import Any

from . import config


def _extract_text(response: Any) -> str:
    return response.content if hasattr(response, "content") else str(response)


def _strip_fences(text: str) -> str:
    return re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip())


def _clean_json_candidate(text: str) -> str:
    """Fix the most common ways models mangle JSON: smart quotes copied from
    the surrounding prose, and trailing commas before a closing bracket."""
    replacements = {
        "\u201c": '"', "\u201d": '"',
        "\u2018": "'", "\u2019": "'",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return re.sub(r",\s*([}\]])", r"\1", text)


def parse_json_response(response: Any) -> dict[str, Any]:
    """Parse a model response as a JSON object, tolerating markdown fences,
    smart quotes, trailing commas, and stray commentary around the object."""
    raw = _extract_text(response)
    cleaned = _clean_json_candidate(_strip_fences(raw))
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not match:
            raise ValueError("The model response did not contain valid JSON.")
        try:
            parsed = json.loads(_clean_json_candidate(match.group(0)))
        except json.JSONDecodeError as exc:
            raise ValueError("The model response did not contain valid JSON.") from exc
    if not isinstance(parsed, dict):
        raise ValueError("The model returned JSON, but not a JSON object.")
    return parsed


_TITLE_RE = re.compile(r"TITLE:\s*(.+)")
_CONTENT_RE = re.compile(r"===BEGIN CONTENT===\s*\n?(.*?)\n?===END CONTENT===", re.DOTALL)
_CHANGES_RE = re.compile(r"===BEGIN CHANGES===\s*\n?(.*?)\n?===END CHANGES===", re.DOTALL)


def parse_delimited_draft(response: Any) -> dict[str, Any]:
    """Parse the TITLE / ===BEGIN CONTENT=== ... ===END CONTENT=== format
    used for draft generation. Word count is always computed locally rather
    than trusted from the model — one less thing that can go wrong."""
    raw = _strip_fences(_extract_text(response))

    content_match = _CONTENT_RE.search(raw)
    content = content_match.group(1).strip() if content_match else raw.strip()

    title_match = _TITLE_RE.search(raw)
    if title_match:
        title = title_match.group(1).strip()
    else:
        first_line = content.split("\n", 1)[0].strip()
        title = first_line[:80] if first_line else "Untitled draft"

    if not content:
        raise ValueError("The model response did not contain any draft content.")

    return {"title": title, "content": content, "word_count": len(content.split())}


def parse_delimited_polish(response: Any) -> dict[str, Any]:
    """Same as parse_delimited_draft, plus an optional CHANGES bullet list."""
    raw = _strip_fences(_extract_text(response))
    result = parse_delimited_draft(raw)

    changes_match = _CHANGES_RE.search(raw)
    changes: list[str] = []
    if changes_match:
        for line in changes_match.group(1).splitlines():
            line = line.strip().lstrip("-*\u2022").strip()
            if line:
                changes.append(line)
    result["changes_summary"] = changes
    return result


def validate_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Normalize and validate the contract between the first two stages."""
    required = ["topic", "audience", "tone", "format", "key_points"]
    missing = [field for field in required if not brief.get(field)]
    if missing:
        raise ValueError(f"Brief is missing: {', '.join(missing)}")
    if brief["tone"] not in config.TONE_OPTIONS or brief["format"] not in config.FORMAT_OPTIONS:
        raise ValueError("Brief contains an unsupported tone or format.")
    if not isinstance(brief["key_points"], list):
        raise ValueError("Brief key_points must be a list.")
    return brief


def validate_quality(quality: dict[str, Any]) -> dict[str, Any]:
    """Normalize the quality-checker output and recompute approval from the
    score so the pass/fail gate can't drift from the stated threshold."""
    score_fields = ["overall_score", "clarity", "audience_fit", "brief_coverage", "voice_consistency"]
    for field in score_fields:
        try:
            quality[field] = max(1, min(10, int(quality.get(field, 0))))
        except (TypeError, ValueError):
            quality[field] = 0
    if not isinstance(quality.get("feedback"), list):
        quality["feedback"] = [str(quality.get("feedback", ""))] if quality.get("feedback") else []
    quality["approved"] = quality["overall_score"] >= config.APPROVAL_THRESHOLD
    return quality
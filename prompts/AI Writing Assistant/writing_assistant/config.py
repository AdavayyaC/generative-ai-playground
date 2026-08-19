"""Shared constants and configuration for the AI writing assistant."""

from __future__ import annotations

TONE_OPTIONS = ["professional", "casual", "technical", "inspirational"]
FORMAT_OPTIONS = ["blog", "email", "report", "social"]
LENGTH_OPTIONS = {
    "Short": "150 to 250 words",
    "Medium": "350 to 500 words",
    "Long": "700 to 900 words",
}
GROQ_MODEL = "openai/gpt-oss-120b"
APPROVAL_THRESHOLD = 7
DEFAULT_MAX_ATTEMPTS = 2

# Each format gets its own structural contract so "email" actually comes back
# looking like an email and "blog" comes back with real sections, instead of
# every format collapsing into one generic paragraph blob.
FORMAT_GUIDANCE: dict[str, str] = {
    "email": (
        "Put a line starting with 'Subject: ' as the first line of content. "
        "Follow with a greeting on its own line, then the body in short "
        "paragraphs (2-4 sentences each), then a sign-off on its own line "
        "(e.g. 'Best,' followed by a name placeholder or the sender's name "
        "if it was given). No headers or bullet lists inside the body unless "
        "the key points are genuinely a list of items."
    ),
    "blog": (
        "Start with a one-line hook, not a summary of the whole post. Use "
        "markdown '##' subheadings to break the post into 2-4 sections, each "
        "covering one key point. End with a short closing paragraph, not a "
        "generic 'in conclusion' recap."
    ),
    "report": (
        "Start with a one-paragraph executive summary. Then a '## Findings' "
        "section with the key points as short bullet points. End with a "
        "'## Recommendation' section of 1-3 sentences stating the concrete "
        "next step."
    ),
    "social": (
        "One short punchy hook line, then 1-3 short supporting lines. No "
        "corporate throat-clearing. End with a single clear call to action. "
        "Keep it well under the length guidance if the length guidance would "
        "make it feel like a caption essay."
    ),
}

VOICE_OPTIONS: dict[str, str] = {
    "Professional": (
        "Polished and precise. Confident, no hedging, no slang. Suitable for "
        "a hiring manager, client, or executive audience."
    ),
    "Human & warm": (
        "Clear and direct but conversational, like a competent person "
        "talking to a peer. Contractions are fine. Avoid corporate jargon "
        "and stiff phrasing."
    ),
    "Concise & direct": (
        "As few words as possible without losing meaning. Short sentences. "
        "No throat-clearing, no restating the question, no filler openers."
    ),
}
DEFAULT_VOICE = "Professional"
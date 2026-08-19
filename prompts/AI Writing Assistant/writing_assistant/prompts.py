"""Prompt templates used by the pipeline.

Two output styles are used deliberately:

- JSON, for short structured data (brief, quality scores) where every field
  is a single word/enum or a short string.
- A plain delimited text format (TITLE: / ===BEGIN CONTENT=== ... ===END
  CONTENT===), for anything containing long free-form prose. Long text with
  quotes, apostrophes, and line breaks packed into a JSON string value is a
  well-known LLM failure mode — models frequently forget to escape an
  apostrophe or a line break, which breaks JSON parsing. Sidestepping JSON
  entirely for the content field removes that failure mode rather than
  patching around it.
"""

from __future__ import annotations

SYSTEM_PROMPT = """You are a professional content strategist and copywriter.

You write clear, compelling content tailored precisely to the target audience.
You never use filler phrases, passive voice, or unnecessary adjectives.
You always follow the requested format exactly.

Each instruction below tells you exactly what output format to use — some
want JSON, some want a plain delimited text format. Follow that format
exactly and add no commentary, headers, or text outside what was asked for.

Few-shot examples of the target style:
1. "Choose three priorities before opening your inbox. Give each one a clear finish line, then protect a short block of focused time. A smaller plan is easier to start and more satisfying to finish."
2. "The launch reached 94% of its adoption goal in the first month. Support requests were concentrated in setup, so the next iteration will add an onboarding checklist and a guided first run."
3. "Hi Maya,\n\nI have attached the revised proposal. The new timeline keeps the research phase focused and gives the team a clear review point on Friday.\n\nBest,\nAlex"
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
useful, with 3 to 5 items. Return only the JSON object, nothing else.

User description: {user_input}
"""

CONTENT_PROMPT = """Write a {format} about {topic} for {audience}.

Key points to cover:
{key_points}

Tone: {tone}
Length guidance: {length_guidance}
Brand voice: {voice_guidance}

Structure requirements for this format:
{format_guidance}

Respond in EXACTLY this plain-text format and nothing else — no JSON, no
markdown code fences, no commentary before or after:

TITLE: <the title on one line>
===BEGIN CONTENT===
<the full {format} content here, multiple paragraphs and markdown formatting are fine>
===END CONTENT===
"""

CONTENT_REVISION_PROMPT = """Revise the {format} about {topic} for {audience}.
The previous draft was reviewed and did not pass quality checks. Address the
reviewer feedback directly while keeping everything that already worked.

Previous draft:
{previous_draft}

Reviewer feedback to address:
{feedback}

Key points to cover:
{key_points}

Tone: {tone}
Length guidance: {length_guidance}
Brand voice: {voice_guidance}

Structure requirements for this format:
{format_guidance}

Respond in EXACTLY this plain-text format and nothing else — no JSON, no
markdown code fences, no commentary before or after:

TITLE: <the title on one line>
===BEGIN CONTENT===
<the full revised {format} content here>
===END CONTENT===
"""

POLISH_PROMPT = """The user is not a native English speaker and has written the
draft below themselves. Rewrite it so it reads as fluent, natural English —
fix grammar, word choice, and sentence flow — WITHOUT changing what they are
actually saying. Do not invent new facts, claims, or details that are not
already in their draft. Keep names, numbers, companies, and specific details
exactly as given.

Format: {format}
Target voice: {voice_guidance}
Structure requirements for this format:
{format_guidance}

User's original draft:
{original_text}

Respond in EXACTLY this plain-text format and nothing else — no JSON, no
markdown code fences, no commentary before or after:

TITLE: <a short title for the polished draft>
===BEGIN CONTENT===
<the polished draft here>
===END CONTENT===
===BEGIN CHANGES===
- <short bullet on what you changed and why>
- <short bullet on what you changed and why>
===END CHANGES===
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
least 7. Be specific and concise in feedback. Return only the JSON object,
nothing else.

Brief: {brief}
Draft: {draft}
"""
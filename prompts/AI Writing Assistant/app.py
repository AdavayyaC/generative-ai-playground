"""Entry point: `streamlit run app.py`.

The implementation is split across the `writing_assistant` package:
    config.py    shared constants (formats, tones, voice presets, thresholds)
    prompts.py   every prompt template used by the pipeline
    parsing.py   response parsing/validation (JSON + delimited plain text)
    model.py     live model construction (Groq via langchain)
    pipeline.py  brief -> draft -> quality-check pipeline, plus polish mode
    ui.py        the Streamlit UI

The re-exports below keep `from app import demo_pipeline, parse_json_response,
validate_brief` working for existing tests without changing test_app.py.
"""

from __future__ import annotations

from writing_assistant.parsing import parse_json_response, validate_brief, validate_quality
from writing_assistant.pipeline import demo_pipeline
from writing_assistant.ui import main

__all__ = [
    "parse_json_response",
    "validate_brief",
    "validate_quality",
    "demo_pipeline",
    "main",
]

if __name__ == "__main__":
    main()
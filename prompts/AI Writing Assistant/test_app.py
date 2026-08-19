import json
from app import demo_pipeline, parse_json_response, validate_brief
def test_parse_json_response_accepts_markdown_fences():
    assert parse_json_response("```json\n{\"title\": \"Hello\"}\n```") == {"title": "Hello"}
def test_validate_brief_accepts_supported_contract():
    brief = {"topic": "Planning", "audience": "Managers", "tone": "professional", "format": "blog", "key_points": ["Start small"]}
    assert validate_brief(brief) == brief
def test_demo_pipeline_returns_json_ready_result():
    brief = {"topic": "Planning", "audience": "Managers", "tone": "professional", "format": "blog", "key_points": ["Start small"]}
    draft, quality = demo_pipeline(brief, "150 to 250 words")
    json.dumps({"brief": brief, "draft": draft, "quality": quality})
    assert quality["approved"] is True
    assert draft["word_count"] == len(draft["content"].split())
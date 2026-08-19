from writing_assistant.parsing import parse_delimited_draft, parse_delimited_polish, parse_json_response


def test_parse_delimited_draft_handles_quotes_and_newlines():
    # This is exactly the kind of content that used to break JSON parsing:
    # apostrophes, quoted dialogue, and multiple paragraphs.
    raw = (
        "TITLE: Why \"showing off\" isn't love\n"
        "===BEGIN CONTENT===\n"
        "## The quiet kind\n\n"
        "Love doesn't need an audience. It's not about saying \"look what I did for you.\"\n\n"
        "It's the small, unannounced things that add up.\n"
        "===END CONTENT===\n"
    )
    result = parse_delimited_draft(raw)
    assert result["title"] == 'Why "showing off" isn\'t love'
    assert "It's the small" in result["content"]
    assert result["word_count"] == len(result["content"].split())


def test_parse_delimited_draft_falls_back_without_markers():
    raw = "Just some content with no markers at all."
    result = parse_delimited_draft(raw)
    assert result["content"] == raw
    assert result["title"] == raw


def test_parse_delimited_polish_extracts_changes():
    raw = (
        "TITLE: Cold email\n"
        "===BEGIN CONTENT===\n"
        "Subject: Application for SDE role\n\nHi, I'm reaching out about the role.\n"
        "===END CONTENT===\n"
        "===BEGIN CHANGES===\n"
        "- Fixed subject-verb agreement\n"
        "- Tightened the opening line\n"
        "===END CHANGES===\n"
    )
    result = parse_delimited_polish(raw)
    assert result["changes_summary"] == [
        "Fixed subject-verb agreement",
        "Tightened the opening line",
    ]
    assert result["content"].startswith("Subject:")


def test_parse_json_response_survives_smart_quotes_and_trailing_comma():
    raw = "{\u201ctitle\u201d: \u201cHello\u201d, \u201ccount\u201d: 3,}"
    assert parse_json_response(raw) == {"title": "Hello", "count": 3}
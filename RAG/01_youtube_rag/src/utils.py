def clean_transcript(text: str) -> str:
    """
    Remove unnecessary spaces.
    """

    text = text.replace("\n", " ")
    text = text.replace("  ", " ")

    return text.strip()
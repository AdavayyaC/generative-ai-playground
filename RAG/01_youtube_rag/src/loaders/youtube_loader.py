from youtube_transcript_api import YouTubeTranscriptApi


def get_video_id(url: str) -> str:
    """Extract the YouTube video ID from the URL."""

    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    else:
        raise ValueError("Invalid YouTube URL")


def load_transcript(video_url: str) -> str:
    """Download the transcript and return it as one string."""

    video_id = get_video_id(video_url)

    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(video_id)

    text = " ".join(
        snippet.text
        for snippet in transcript.snippets
    )

    if not text.strip():
        raise ValueError("Transcript is empty.")

    return text


def save_transcript(text: str, file_path: str):
    """Save transcript to a text file."""

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
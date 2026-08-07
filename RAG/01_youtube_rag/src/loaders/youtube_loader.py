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

    # ✅ NEW API (v1.0+): Instantiate the class and use .fetch()
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)

    # In v1.0+, fetch() returns a FetchedTranscript object
    # Each snippet has a .text attribute instead of ["text"]
    text = " ".join(snippet.text for snippet in transcript.snippets)

    return text
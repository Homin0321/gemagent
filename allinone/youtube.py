import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def get_youtube_id(url: str) -> str | None:
    """
    Extracts the video ID from a YouTube URL using urllib.parse for robustness.

    Args:
        url: The YouTube video URL.

    Returns:
        The video ID as a string, or None if not found.
    """
    parsed_url = urlparse(url)

    # Handle shortened youtu.be URLs first for efficiency
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:] # Remove leading slash

    # Handle standard watch URLs
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            if 'v' in query_params:
                return query_params['v'][0]
        elif parsed_url.path.startswith('/shorts/'):
            # Handle YouTube Shorts URLs
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/embed/'):
            # Handle embedded URLs
            return parsed_url.path.split('/')[2]

    return None

def get_youtube_transcript(youtube_url: str) -> str:
    """
    Retrieves YouTube video transcript as plain text from a given URL.
    Prioritizes a list of languages and falls back to the first available.

    Args:
        youtube_url: The URL of the YouTube video (e.g., "https://www.youtube.com/watch?v=dQw4w9WgXcQ").

    Returns:
        The transcript text without time information.
        Returns an empty string if the transcript cannot be found or an error occurs.
    """
    try:
        video_id = get_youtube_id(youtube_url)

        if not video_id:
            print(f"Error: Could not extract video ID from YouTube URL: {youtube_url}")
            return ""

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Define preferred language order
        preferred_languages = ['ko', 'en']
        selected_transcript = None
        selected_language_code = None

        # Iterate through preferred languages to find an available transcript.
        for lang_code in preferred_languages:
            try:
                selected_transcript = transcript_list.find_transcript([lang_code])
                selected_language_code = lang_code
                # Once a transcript in a preferred language is found, exit the loop.
                break
            except NoTranscriptFound:
                # If a transcript for the current language is not found, try the next one.
                continue

        # If no transcript was found in the preferred languages, fall back to the first available one.
        if selected_transcript is None:
            try:
                # find_transcript() without arguments finds the first transcript in the list.
                selected_transcript = transcript_list.find_transcript()
                selected_language_code = selected_transcript.language_code
            except NoTranscriptFound:
                print(f"Error: No transcript found for video ID: {video_id} in any language.")
                return ""

        # Fetch the transcript data and join the text segments into a single string.
        # A list comprehension and join is an efficient way to build the string.
        transcript_entries = selected_transcript.fetch()
        transcript_text = " ".join([entry.text for entry in transcript_entries])

        return transcript_text.strip()

    except NoTranscriptFound as e:
        print(f"Error: No transcript available for video: {youtube_url}. Details: {e}")
        return ""
    except Exception as e:
        # Catch other potential errors like network issues, invalid video IDs, etc.
        print(f"An unexpected error occurred while fetching the transcript for {youtube_url}: {e}")
        return ""
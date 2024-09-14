import re
import yt_dlp


def yt_dlp_extract_audio_url(url):
    ydl_opts = {"format": "bestaudio", "quiet": True}

    return yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)["url"]


def extract_video_id(url):
    # Patterns for different types of YouTube URLs
    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)",  # Standard watch URL
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)",  # Embed URL
        r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)",  # Shortened URL
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^?]+)",  # Old embed URL
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([^?]+)",  # Shorts URL
    ]

    # Try each pattern
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # If no match is found
    return None

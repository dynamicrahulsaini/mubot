import logging
import re
import yt_dlp

def extract_song_info(url):
    """Extract song information from YouTube URLs"""
    if 'youtube.com' in url or 'youtu.be' in url:
        return extract_youtube_info(url)
    return None

def extract_youtube_info(url):
    """Extract song information from YouTube URL"""
    ydl_opts = {
        "format": "bestaudio",
        "quiet": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
        "extract_flat": False,
        "cookiesfrombrowser": ("chrome", None, None, None),  # Fixed browser cookies configuration
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'url': info['url'],
                'title': info.get('title', 'Unknown Title'),
                'artist': info.get('uploader', 'Unknown Artist'),
                'source': 'youtube'
            }
    except Exception as e:
        logging.error(f"Error extracting YouTube audio URL: {str(e)}")
        return None

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

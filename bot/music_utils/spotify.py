import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bot.secrets import Secrets

# Initialize Spotify client
secrets = Secrets()
spotify = None
if secrets.spotify_client_id and secrets.spotify_client_secret:
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=secrets.spotify_client_id,
        client_secret=secrets.spotify_client_secret
    ))

def search_by_title(title):
    """Search Spotify using a title and return the first result"""
    if not spotify:
        logging.error("Spotify credentials not configured")
        return None

    try:
        results = spotify.search(q=title, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            # Get the preview URL if available
            preview_url = track.get('preview_url')
            if preview_url:
                return {
                    'url': preview_url,
                    'title': track['name'],
                    'artist': track['artists'][0]['name'],
                    'source': 'spotify',
                    'track_id': track['id']
                }
            else:
                logging.warning(f"No preview URL available for track: {track['name']}")
                return None
    except Exception as e:
        logging.error(f"Error searching Spotify: {str(e)}")
    return None

def extract_track_info(url):
    """Extract song information from Spotify URL"""
    if not spotify:
        logging.error("Spotify credentials not configured")
        return None

    try:
        # Extract track ID from URL
        track_id = url.split('/')[-1].split('?')[0]
        track = spotify.track(track_id)
        
        # Get the preview URL if available
        preview_url = track.get('preview_url')
        if preview_url:
            return {
                'url': preview_url,
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'source': 'spotify',
                'track_id': track['id']
            }
        else:
            logging.warning(f"No preview URL available for track: {track['name']}")
            return None
    except Exception as e:
        logging.error(f"Error extracting Spotify track info: {str(e)}")
        return None 
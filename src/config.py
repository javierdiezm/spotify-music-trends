import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv(override=True)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Spotify client ID and secret must be set in the .env file.")

def get_spotify_client():
    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET)
    return spotipy.Spotify(auth_manager=auth_manager)
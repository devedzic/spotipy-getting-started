"""Functions for Spotify authentication.
"""


#%%
# Import statements

import os

from pathlib import Path
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


#%%
def get_spotify_object(env_file_path: str) -> spotipy.client.Spotify:

    env_file = Path(Path.cwd().parent) / env_file_path
    load_dotenv(env_file)

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)



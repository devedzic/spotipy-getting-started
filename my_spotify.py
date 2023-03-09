"""Functions for Spotify authentication, getting tracks from a playlist, etc.
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


#%%
def get_all_tracks_from_playlist(playlist_id: str, env_file_path: str) -> list:
    spot = get_spotify_object(env_file_path)
    offset = 0
    all_tracks = []
    tracks = spot.playlist_items(playlist_id, offset=offset)           # the first 100 tracks (offset = 0)
    if not tracks['items']:                                             # if the playlist is empty
        return []
    all_tracks.extend(tracks['items'])
    while tracks['next']:
        offset += 100
        tracks = spot.playlist_items(playlist_id, offset=offset)       # the next 100 tracks
        all_tracks.extend(tracks['items'])
    return all_tracks


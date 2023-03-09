"""Functions for Spotify authentication, getting tracks from a playlist, getting tracks data and audio features, etc.
"""


#%%
# Import statements

import os

from pathlib import Path
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import pandas as pd


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


#%%
def get_tracks_data(playlist_id: str, env_file_path: str) -> list:
    tracks = get_all_tracks_from_playlist(playlist_id, env_file_path)
    tracks_data = [(t['track']['uri'],
                    t['track']['name'].split(' - Remastered')[0].split(' / Remastered')[0],
                    t['track']['popularity'],
                    int(round(t['track']['duration_ms'] / 1000, 0))) for t in tracks]
    return tracks_data


#%%
def get_tracks_audio_features(playlist_id: str, env_file_path: str) -> list:
    spot = get_spotify_object('env/.env')
    tracks = get_all_tracks_from_playlist(playlist_id, env_file_path)
    uri_list = [t['track']['uri'] for t in tracks]

    offset = 0
    runs, last_run = divmod(len(tracks), 100)                                                       # how many full runs, 100 tracks each
    tracks_audio_features_dicts = []

    if runs > 0:                                                                                    # all full runs, 100 tracks each
        for _ in range(runs):
            tracks_audio_features_dicts.extend(spot.audio_features(uri_list[offset:(offset+100)]))
            offset += 100
    tracks_audio_features_dicts.extend(spot.audio_features(uri_list[offset:(offset+last_run)]))     # last run, < 100 tracks

    tracks_audio_features = [(t['key'],
                              t['mode'],
                              t['tempo'],
                              t['time_signature'],
                              t['valence'],
                              t['danceability'],
                              t['energy'],
                              t['loudness'],
                              t['acousticness'],
                              t['instrumentalness'],
                              t['liveness'],
                              t['speechiness']) for t in tracks_audio_features_dicts]

    return tracks_audio_features


#%%
def get_tracks_df(playlist_id: str, env_file_path: str) -> pd.DataFrame:
    tracks_data = get_tracks_data(playlist_id, env_file_path)
    tracks_audio_features = get_tracks_audio_features(playlist_id, env_file_path)
    tracks_data_and_audio_features = [(d + af) for d, af in zip(tracks_data, tracks_audio_features)]
    return pd.DataFrame(tracks_data_and_audio_features,
                        columns=[
                            'URI',
                            'Title',
                            'Popularity',
                            'Duration',
                            'Key',
                            'Mode',
                            'Tempo',
                            'time_signature',
                            'valence',
                            'danceability',
                            'energy',
                            'loudness',
                            'acousticness',
                            'instrumentalness',
                            'liveness',
                            'speechiness'
                        ])

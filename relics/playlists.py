import os

from pathlib import Path
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from my_spotify import get_spotify_object


#%%
print(get_spotify_object('env/.env'))

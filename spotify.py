import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlist import Playlist
from typing import List
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from logging_config import log

client_id = os.getenv("AI_PLAYLIST_SPOTIPY_CLIENT_ID")
client_secret = os.getenv("AI_PLAYLIST_SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("AI_PLAYLIST_SPOTIPY_REDIRECT_URL")
log.debug(f"Redirect URL for authorization flow: {redirect_uri}")

auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-modify-private playlist-modify-public"
)

sp = spotipy.Spotify(auth_manager=auth_manager)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_spotify_track_ids(playlist: Playlist) -> List[str]:
    track_ids = []

    # search for each song in the playlist
    for song in playlist.songs:
        query = f"{song.title} artist:{song.artist}"

        log.info(f"Searching for song with query: {query}")
        result = sp.search(q=query, type="track", limit=1)
        log.info(f"Result returned for song from Spotify search: {result}")

        # if the search returns no results, we can skip this iteration
        if result["tracks"]["total"] < 1:
            log.warn(f"Could not find any result for query: {query}")
            continue

        track_id = result["tracks"]["items"][0]["id"]
        track_ids.append(track_id)

    return track_ids

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def create_spotify_playlist(track_ids: List[str], title: str, description: str) -> str:
    log.info(f"Creating playlist from track_ids: {track_ids}")
    user_id = sp.me()["id"]

    # create playlist
    new_playlist = sp.user_playlist_create(
        user=user_id,
        name=title,
        public=False,
        description=description
    )
    log.info(f"New playlist returned from Spotify: {new_playlist}")

    # add the tracks to the playlist
    sp.playlist_add_items(playlist_id=new_playlist["id"], items=track_ids)

    # return the link to the playlist
    return new_playlist["external_urls"]["spotify"]
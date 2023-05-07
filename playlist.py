import json
from dataclasses import dataclass
from typing import List

@dataclass
class Song:
    title: str
    artist: str

@dataclass
class Playlist:
    title: str
    description: str
    songs: List[Song]

def convert_dict_to_playlist(playlist_dict: str) -> Playlist:
    songs = [Song(**song_dict) for song_dict in playlist_dict["songs"]]
    return Playlist(
        title=playlist_dict["title"],
        description=playlist_dict["description"],
        songs=songs)


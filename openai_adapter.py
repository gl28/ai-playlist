import openai
import os
import json
from typing import Dict, Any
from playlist import Playlist, Song, convert_dict_to_playlist
from spotify import get_spotify_track_ids, create_spotify_playlist

openai.api_key = os.getenv("OPENAI_API_KEY")

example_playlist = {
    "title" : "title of playlist",
    "description" : "description of playlist",
    "songs": [
        {
            "title": "first song title",
            "artist": "first song artist"
        },
        {
            "title": "second song title",
            "artist": "second song artist"
        }
    ]
}

system_prompt = f"""You are an playlist creation AI.

You should take the user's input and try to come up with a playlist of 30 songs that
matches their description.

You should only return songs which actually exist.

You should also include a title and a one sentence description of the playlist.

Your response should be a JSON object formatted as follows:
{json.dumps(example_playlist)}
"""

def get_playlist_json(user_prompt: str) -> str:
    print(f"Calling OpenAI to get JSON formatted playlist for prompt: {user_prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    assistant_response = response['choices'][0]['message']['content']
    print(f"OpenAI JSON playlist response: {assistant_response}")
    return assistant_response

if __name__ == "__main__":
    user_input = input("Enter your request for a playlist: ")
    suggested_playlist = get_playlist_json(user_input)
    print(f"Suggested playlist: {suggested_playlist}")
    playlist = convert_dict_to_playlist(suggested_playlist)
    print(f"Final playlist: {playlist}")

    tracks = get_spotify_track_ids(playlist)
    print(tracks)


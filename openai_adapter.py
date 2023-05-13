import openai
import os
import json
import time
from tenacity import retry, stop_after_attempt, wait_exponential
from logging_config import log

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

system_prompt = f"""You are a playlist creation AI.

You should take the user's input and try to come up with a playlist of 30 songs that
matches their description.

You should only return songs which actually exist.

You should also include a title and a one sentence description of the playlist.

Your response should be a JSON object formatted as follows:
{json.dumps(example_playlist)}
"""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_playlist_json(user_prompt: str) -> str:
    start = time.time()
    log.info(f"Calling OpenAI to get JSON formatted playlist for prompt: {user_prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    assistant_response = response['choices'][0]['message']['content']
    log.info(f"Calling OpenAI to get playlist took: {(time.time() - start) * 1000} ms")
    log.info(f"OpenAI JSON playlist response: {assistant_response}")
    return assistant_response
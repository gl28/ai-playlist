import os
from flask import Flask, request, redirect, session, render_template
from openai_adapter import get_playlist_json
from playlist import convert_dict_to_playlist, Playlist
from spotify import auth_manager, create_spotify_playlist, get_spotify_track_ids
from logging_config import log

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    if not refresh_token():
        return redirect("/login")
    
    return render_template("create_playlist.html", input="")

@app.route("/get_playlist_suggestions")
def get_playlist_suggestions():
    input_text = request.args.get("input", "")
    return get_playlist_json(input_text)

@app.route("/create_spotify_playlist_from_json", methods=["POST"])
def create_spotify_playlist_from_json():
    playlist_dict = request.json.get("input", "")
    log.debug(f"Playlist data received by API: {playlist_dict}")

    playlist = convert_dict_to_playlist(playlist_dict)
    track_ids = get_spotify_track_ids(playlist)
    log.debug(f"Creating playlist for {len(track_ids)} track ids: {track_ids}")
    
    playlist_link = create_spotify_playlist(track_ids, playlist.title, playlist.description)
    return playlist_link

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/authorize")
def authorize():
    log.info("Beginning authorization flow...")
    auth_url = auth_manager.get_authorize_url()
    log.debug(f"Auth url {auth_url}")
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = auth_manager.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/")

def refresh_token():
    token_info = session.get("token_info", None)
    if not token_info:
        return False

    if auth_manager.is_token_expired(token_info):
        token_info = auth_manager.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    return True

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG_MODE", default=False))

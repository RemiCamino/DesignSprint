from fastapi import FastAPI, HTTPException, Query
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client_id = '88d09a98f3a342d099d4ee707ded9d89'
client_secret = '60daea895d7d4435a6f51c4ee664ff1c'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-top-read playlist-modify-private'

auth_manager = SpotifyOAuth(
    client_id=client_id, 
    client_secret=client_secret, 
    redirect_uri=redirect_uri, 
    scope=scope
)

sp = spotipy.Spotify(auth_manager=auth_manager)

class CreatePlaylistRequest(BaseModel):
    playlist_name: Optional[str] = "SHUFFLEMAX"

@app.post("/create_playlist")
def create_playlist(request: CreatePlaylistRequest):
    playlist_name = request.playlist_name
    try:
        top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=25)
        top_tracks_ids = [track['id'] for track in top_tracks['items']]

        recommended_tracks = []
        for track_id in top_tracks_ids:
            try:
                recommendations = sp.recommendations(seed_tracks=[track_id], limit=1)
                recommended_track = recommendations['tracks'][0]
                recommended_tracks.append(recommended_track['id'])
            except spotipy.exceptions.SpotifyException as e:
                print(f"Error getting recommendations for {track_id}: {e}")

        all_track_ids = top_tracks_ids + recommended_tracks
        random.shuffle(all_track_ids)

        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
        sp.playlist_add_items(playlist_id=playlist['id'], items=all_track_ids)

        return {"message": "Playlist created successfully", "playlist_id": playlist['id']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import json

@app.get("/callback")
def handle_callback(code: str = Query(...)):
    try:
        token_info = auth_manager.get_access_token(code)
        return {"message": "Authentication successful", "token_info": token_info}
    except spotipy.oauth2.SpotifyOauthError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_token")
def get_token():
    try:
        with open('token_info.json', 'r') as file:
            token_info = json.load(file)
        return token_info
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Token not found")

@app.get("/get_user_profile")
def get_user_profile():
    try:
        user_profile = sp.current_user()
        return user_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

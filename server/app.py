from fastapi import FastAPI, HTTPException
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

client_id = 'd72df51fb9c24183a83bb23a4663925c'
client_secret = 'a2f4aed62807411893b7c2e4c8425350'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-top-read playlist-modify-private'

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

class CreatePlaylistRequest(BaseModel):
    genre: str
    playlist_name: str

@app.post("/create_playlist")
def create_playlist(request: CreatePlaylistRequest):
    genre = request.genre
    playlist_name = request.playlist_name
    try:
        top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=25)
        top_tracks_ids = [track['id'] for track in top_tracks['items']]

        filtered_tracks_ids = []
        for track_id in top_tracks_ids:
            track_features = sp.audio_features(track_id)[0]
            if track_features and track_features['genre'] == genre:
                filtered_tracks_ids.append(track_id)

        recommended_tracks = []
        for track_id in filtered_tracks_ids:
            try:
                recommendations = sp.recommendations(seed_tracks=[track_id], limit=1)
                recommended_track = recommendations['tracks'][0]
                recommended_tracks.append(recommended_track['id'])
            except spotipy.exceptions.SpotifyException as e:
                print(f"Error getting recommendations for {track_id}: {e}")

        all_track_ids = filtered_tracks_ids + recommended_tracks
        random.shuffle(all_track_ids)

        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

        sp.playlist_add_items(playlist_id=playlist['id'], items=all_track_ids)

        return {"message": "Playlist created successfully", "playlist_id": playlist['id']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

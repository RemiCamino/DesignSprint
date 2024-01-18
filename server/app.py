from fastapi import FastAPI, HTTPException
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

app = FastAPI()

client_id = 'd72df51fb9c24183a83bb23a4663925c'
client_secret = 'a2f4aed62807411893b7c2e4c8425350'
redirect_uri = 'http://localhost:5000/callback'
scope = 'user-top-read playlist-modify-private'

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

@app.get("/top_tracks")
def get_top_tracks():
    try:
        top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=25)
        return top_tracks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_playlist")
def create_playlist():
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

        playlist_name = "SHUFFLEMAX"
        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

        sp.playlist_add_items(playlist_id=playlist['id'], items=all_track_ids)

        return {"message": "Playlist created successfully", "playlist_id": playlist['id']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

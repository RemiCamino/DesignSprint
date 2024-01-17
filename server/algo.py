import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Set up your Spotify API credentials
client_id = 'd72df51fb9c24183a83bb23a4663925c'
client_secret = 'a2f4aed62807411893b7c2e4c8425350'
redirect_uri = 'http://localhost:5000/callback'

# Set up authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-top-read playlist-modify-private'))

# Get the user's top tracks
top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=25)

# Print the details of top_tracks
print("Top Tracks:")
for idx, track in enumerate(top_tracks['items'], start=1):
    print(f"{idx}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
    print(f"   Track ID: {track['id']}")
# Extract the track IDs from the top tracks
top_tracks_ids = [track['id'] for track in top_tracks['items']]

# Loop through each track and get recommendations
recommended_tracks = []
for track_id in top_tracks_ids:
    try:
        # Get recommendations based on the current track
        recommendations = sp.recommendations(seed_tracks=[track_id], limit=1)

        # Extract the recommended track details
        recommended_track = recommendations['tracks'][0]
        recommended_tracks.append(recommended_track['id'])
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error getting recommendations for {track_id}: {e}")
        print(f"Request details: {e.http_status}, {e.code}, {e.msg}, {e.reason}")

# Combine the top tracks and recommended tracks
all_track_ids = top_tracks_ids + recommended_tracks

# Shuffle the track IDs randomly
random.shuffle(all_track_ids)

# Create a playlist named "SHUFFLEMAX"
playlist_name = "SHUFFLEMAX"
playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=False)

# Add tracks to the playlist
sp.playlist_add_items(playlist_id=playlist['id'], items=all_track_ids)

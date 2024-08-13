import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config


def get_top_tracks(sp, playlist_id):
    # Fetch the top tracks from the specified playlist
    results = sp.playlist_tracks(playlist_id, limit=50)
    tracks = []
    for idx, item in enumerate(results['items']):
        track = item['track']
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity']
        })
    return tracks


def main():
    # Authenticate with Spotify using the credentials from config.py
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config.SPOTIPY_CLIENT_ID,
        client_secret=config.SPOTIPY_CLIENT_SECRET,
        redirect_uri=config.SPOTIPY_REDIRECT_URI,
    ))

    playlist_id = '37i9dQZEVXbMDoHDwVN2tF'  # Global Top 50 Playlist ID

    top_tracks = get_top_tracks(sp, playlist_id)

    for idx, track in enumerate(top_tracks):
        print(f"{idx + 1}. {track['name']} by {track['artist']} - Popularity: {track['popularity']}")


if __name__ == "__main__":
    main()

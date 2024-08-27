import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import config


def authenticate_spotify() -> spotipy.Spotify:
    client_id = config.SPOTIPY_CLIENT_ID
    client_secret = config.SPOTIPY_CLIENT_SECRET
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)


def create_database_connection(db_name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    return conn


def create_table(cursor: sqlite3.Cursor):
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS top_tracks (
        id TEXT PRIMARY KEY,
        name TEXT,
        artist TEXT,
        album TEXT,
        genre TEXT,
        popularity INTEGER,
        load_timestamp TEXT
    );
    '''
    cursor.execute(create_table_query)


def extract_top_tracks(sp: spotipy.Spotify) -> list:
    results = sp.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF', limit=50)
    return results['items']


def transform_track_data(track: dict, sp: spotipy.Spotify) -> tuple:
    track_id = track['track']['id']
    track_name = track['track']['name']
    artist_name = track['track']['artists'][0]['name']
    album_name = track['track']['album']['name']
    popularity = track['track']['popularity']

    artist_id = track['track']['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    genres = artist_info['genres']
    genre_str = ', '.join(genres) if genres else 'Unknown'

    load_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return (track_id, track_name, artist_name, album_name, genre_str, popularity, load_timestamp)


def load_data(cursor: sqlite3.Cursor, track_data: tuple):
    insert_query = '''
    INSERT OR IGNORE INTO top_tracks (id, name, artist, album, genre, popularity, load_timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, track_data)


def main():
    sp = authenticate_spotify()
    conn = create_database_connection('spotify_data.db')
    cursor = conn.cursor()

    create_table(cursor)

    top_tracks = extract_top_tracks(sp)

    for item in top_tracks:
        track_data = transform_track_data(item, sp)
        load_data(cursor, track_data)

    conn.commit()

    # Optionally, you can verify the data
    cursor.execute('SELECT * FROM top_tracks')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()


if __name__ == "__main__":
    main()

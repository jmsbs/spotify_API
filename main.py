import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import config

# Set up Spotify API credentials from the config file
client_id = config.SPOTIPY_CLIENT_ID
client_secret = config.SPOTIPY_CLIENT_SECRET

# Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('spotify_data.db')
cursor = conn.cursor()

# 3. Create a table for storing Spotify top tracks with additional information
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
conn.commit()

# Fetch top 50 daily tracks from Spotify API
results = sp.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF', limit=50)  # Spotify Global Top 50 Playlist

# Extract and insert data into the SQLite database with a load timestamp
load_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current timestamp

for item in results['items']:
    track = item['track']
    track_id = track['id']
    track_name = track['name']
    artist_name = track['artists'][0]['name']
    album_name = track['album']['name']
    popularity = track['popularity']

    # Fetch genre from the artist's data
    artist_id = track['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    genres = artist_info['genres']
    genre_str = ', '.join(genres) if genres else 'Unknown'

    # Insert data into the SQLite table
    insert_query = '''
    INSERT OR IGNORE INTO top_tracks (id, name, artist, album, genre, popularity, load_timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (track_id, track_name, artist_name, album_name, genre_str, popularity, load_timestamp))

# Commit the transaction
conn.commit()

# Query the database to verify the insertion
cursor.execute('SELECT * FROM top_tracks')
rows = cursor.fetchall()

# Print the data retrieved from the database
for row in rows:
    print(row)

# Close the connection
conn.close()

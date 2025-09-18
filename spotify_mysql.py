import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='39f65947fa9f4ce2ba4d073d3a0fb53a',  
    client_secret='d580810c7f954d5da5e212b91620b252'  
))

db_config = {
    'host': 'localhost',           
    'user': 'root',       
    'password': '1508',   
    'database': 'spotify_db'  
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

track_url = "https://open.spotify.com/track/7fUS9gftrrgtaHJUwFnbEt"

track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

track = sp.track(track_id)

track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

insert_query = """
INSERT INTO track_data (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)']
))
connection.commit()

print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")

cursor.close()
connection.close()

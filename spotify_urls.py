import re
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='7ae955693f224b679fc0abaad6996b13',  
    client_secret='a4b9348c27754ccb92abe396752c15c4'  
))

db_config = {
    'host': 'localhost', 
    'user': 'root',     
    'password': '1508', 
    'database': 'spotify_db'       
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

file_path = "track_urls.txt"
with open(file_path, 'r') as file:
    track_urls = file.readlines()

for track_url in track_urls:
    track_url = track_url.strip()  
    try:
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

        print(f"Inserted: {track_data['Track Name']} by {track_data['Artist']}")

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

cursor.close()
connection.close()

print("All tracks have been processed and inserted into the database.")
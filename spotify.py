from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import matplotlib.pyplot as plt
import pandas as pd
import re
# import json

sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(
    client_id = '39f65947fa9f4ce2ba4d073d3a0fb53a', 
    client_secret = 'd580810c7f954d5da5e212b91620b252'
))

track_url = "https://open.spotify.com/track/7fUS9gftrrgtaHJUwFnbEt"

track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

track = sp.track(track_id)
print(track)

# with open("track_data.json", "w", encoding="utf-8") as f:
#     json.dump(track, f, indent=4, ensure_ascii=False)

track_data = {
    'Track Name' : track['name'],
    'Artist' : track['artists'][0]['name'],
    'Album' : track['album']['name'],
    'Popularity' : track['popularity'],
    'Duration (minutes)' : track['duration_ms']/60000
}

print(f"\nTrack Name: {track_data['Track Name']}")
print(f"Artist: {track_data['Artist']}")
print(f"Album: {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Duration: {track_data['Duration (minutes)']:.2f} minutes")

df = pd.DataFrame([track_data])
print("\nTrack Data as DataFrame:")
print(df)

df.to_csv('tracks.csv', index=False)

features = ['Popularity', 'Duration (minutes)']
values = [track_data['Popularity'], track_data['Duration (minutes)']]

plt.figure(figsize=(8, 5))
plt.bar(features, values, color='skyblue', edgecolor='black')
plt.title(f"Track Metadata for '{track_data['Track Name']}'")
plt.ylabel('Value')
plt.show()

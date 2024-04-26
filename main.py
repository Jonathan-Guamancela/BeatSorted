import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Authentication with Spotify
auth_manager = SpotifyClientCredentials(client_id='Your client ID', client_secret='Your Secret Client ID')
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_track_info(track_id):
    try:
        features = sp.audio_features(track_id)[0]
        if features:
            return (features['tempo'], features['key'])
        else:
            return (None, None)  # Return None if audio features are missing
    except Exception as e:
        print(f"Error retrieving track info for {track_id}: {str(e)}")
        return (None, None)


playlist_id = 'Your playlist ID here'  # Replace with your playlist ID
tracks = get_playlist_tracks(playlist_id)
track_details = []

print("Using playlist ID:", playlist_id)
results = sp.playlist_tracks(playlist_id)


for track in tracks:
    track_id = track['track']['id']
    bpm, key = get_track_info(track_id)
    track_details.append({'name': track['track']['name'], 'bpm': bpm, 'key': key})

# Example sorting by BPM
sorted_by_bpm = sorted(track_details, key=lambda x: x['bpm'])
# Example sorting by Key, then BPM
sorted_by_key_bpm = sorted(track_details, key=lambda x: (x['key'], x['bpm']))

# Print sorted lists or process further as needed
print("Name\t\t\t\tKey\tBPM")
for track in sorted_by_key_bpm:
    print(f"{track['name'][:30]:30}\t{track['key']}\t{track['bpm']}")


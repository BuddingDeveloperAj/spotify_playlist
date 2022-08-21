import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input('Enter the date in format YYYY-MM-DD: ')
song_url = f"https://www.billboard.com/charts/hot-100/{date}"

Client_ID = "Secret ID"
Client_Secret = "Secret Key"

response = requests.get(url=song_url)
data = response.text

soup = BeautifulSoup(data, "html.parser")
songs = soup.select("h3#title-of-a-story.c-title.a-no-trucate")
songs_list = []
for song in songs:
    song = song.getText().strip()
    songs_list.append(song)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID,
                                               client_secret=Client_Secret,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path=".cache",
                                               ))

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
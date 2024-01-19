import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id = "0axxxxxxxxxxxxxxxxxxe4a"
spotify_client_secret = "2xxxxxxxxxxxxxxxxxxxxxxxxxxxxx6cdd"

URL = "https://in.soundpasta.com/2020/09/top-100-best-hindi-songs-of-all-time-the-definitive-list-of-indian-music/"

spotify_auth_user = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"

    )
)

auth_token_dict = spotify_auth_user.current_user()
# print(user)
user_id = auth_token_dict["id"]
# print(user_id)

# ______________________________searching song from internet________________________

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6"
}

response = requests.get(url=URL, headers=header)
content = response.text
# print(content)

soup = BeautifulSoup(content, "html.parser")

top_song = soup.find_all(name="h3")
# print(top_song)

songs_list = []
for song in top_song:
    try:
        songs_list.append(song.getText().split(")")[-1])
    except:
        pass
print(songs_list)
print(len(songs_list))

# _________________________search songs_______________________

song_uri_list = []

for title in songs_list[0:98]:  # maximum limit is 100
    # print(title)
    result = spotify_auth_user.search(q=f"track:{title}", type="track")

    try:
        uri = result['tracks']['items'][0]['uri']
        song_uri_list.append(uri)
    except:
        print("song not found")
# print(song_uri_list)

# _______________________ create playlist ____________________

playlist = spotify_auth_user.user_playlist_create(user=user_id, name=f"py generated 100 hindi songs", public=False)
# print(playlist)

# _____________ adding songs in playlist ______________________

result = spotify_auth_user.playlist_add_items(playlist_id=playlist["id"], items=song_uri_list)
print(result)

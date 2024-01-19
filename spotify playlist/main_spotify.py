import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_client_id = "0axxxxxxxxxxxxxxxx376e4a"
spotify_client_secret = "xxxxxxxxxxxxxxxxxxxxdd"

user_date = input("enter date in yyyy-mm-dd form: ")
URL = f"https://www.billboard.com/charts/hot-100/{user_date}/"
year = user_date.split("-")[0]

# URL = f"https://www.billboard.com/charts/hot-100/2004-01-2/"
# year = 2004

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

# ______________________________searching songs from billboard________________________

response = requests.get(url=URL)
content = response.text
# print(content)
soup = BeautifulSoup(content, "html.parser")

top_song = ((soup.find(name="a", class_="c-title__link lrv-a-unstyle-link")).getText()).strip()
other_song_tag = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
# print(song_title_tag)

songs_list = [top_song]
for song in other_song_tag:
    try:
        songs_list.append(song.getText().strip())
    except:
        pass
print(songs_list)
print(len(songs_list))

# _________________________search songs_______________________

song_uri_list = []

for title in songs_list[0:25]:
    # print(title)
    result = spotify_auth_user.search(q=f"track:{title} year:{year}", type="track", limit=1)

    try:
        uri = result['tracks']['items'][0]['uri']
        song_uri_list.append(uri)
    except:
        print("song not found")
# print(song_uri_list)

# _______________________ create playlist ____________________

playlist = spotify_auth_user.user_playlist_create(user=user_id, name=f"year {year} Billboard 25 songs", public=False)
print(playlist)

# _____________ adding songs in playlist ______________________

result = spotify_auth_user.playlist_add_items(playlist_id=playlist["id"], items=song_uri_list)
print(result)

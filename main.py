from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
TOKEN = ''

def getToken():
    authString = clientID + ":" + clientSecret
    authBytes = authString.encode("utf-8")
    authBase64 = str(base64.b64encode(authBytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authBase64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    jsonResult = json.loads(result.content)
    token = jsonResult["access_token"]
    return token

def getAuthHeader(token):
    return {"Authorization": "Bearer " + token}

def getPlaylists(token):
    flag = True
    playlists = []
    offset = 0
    while flag:
        url=f"https://api.spotify.com/v1/users/nerd-e/playlists?limit=50&offset={offset}"
        headers=getAuthHeader(TOKEN)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)["items"]
        if (len(jsonResult)!=50):
            flag = False
        offset += 50
        playlists.extend(jsonResult)
        print("Getting playlists: ", offset)
    return playlists

def getPlaylistSongs(token, playlistID):
    flag = True
    songs = []
    offset = 0
    while flag:
        url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?offset={offset}"
        headers = getAuthHeader(TOKEN)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)["items"]
        if (len(jsonResult)!=100):
            flag = False
        offset += 100
        songs.extend(jsonResult)
    return songs

def createPlaylist():
    url = "https://api.spotify.com/v1/users/nerd-e/playlists"
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json"
        }
    data = {
        "name": "Lost in Liked™",
        "description": "some cheesy quote about being lost | github link",
        "public": "true"
        }
    result = post(url, headers=headers, data=json.dumps(data))
    return json.loads(result.content)['id']

def addSongs(playlistID, uris):
    url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?uris=" + uris
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json"
        }
    result = post(url, headers=headers)

def getLikedSongs():
    flag = True
    songs = []
    offset = 0
    while flag:
        url=f"https://api.spotify.com/v1/me/tracks?limit=50&offset={offset}"
        headers=getAuthHeader(TOKEN)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)["items"]
        if (len(jsonResult)!=50):
            flag = False
        offset += 50
        songs.extend(jsonResult)
        print("Getting Liked Songs: ", offset)
    return songs

token = getToken()
liked = getLikedSongs()

print('Getting Playlists...')
result = getPlaylists(token)


playlistMade = False
for playlist in result:
    if playlist["name"] == "Lost in Liked™":
        playlistMade = True
        newPlaylistID = playlist['id']
        print(f'Found Playlist...{newPlaylistID}')
if not playlistMade:
    newPlaylistID = createPlaylist()
    print(f'Creating New Playlist... {newPlaylistID}')

playlistIDs  = []
likedURIs = []
songURIs = []


for idx, playlist in enumerate(result):
    if idx%100 == 0:
        print("Progress: ", idx)
    playlistIDs.append(playlist["id"])
    songs = getPlaylistSongs(token, playlist["id"])
    print(f"Playlist {idx+1}...")
    for jdx, song in enumerate(songs):
        try:
            newSong = song['track']['uri']
            if newSong not in songURIs:
                songURIs.append(newSong)
        except:
            print("something went wrong ----- continuing")

print('URIs Obtained...')

for idx, song in enumerate(liked):
    if idx%100 == 0:
        print("Progress: ", idx)
    newSong = song['track']['uri']
    if newSong not in songURIs:
        likedURIs.append(newSong)

print('Liked Songs Put in List...')

uris = ""
for idx, song in enumerate(likedURIs):
    if idx%100 == 0 and idx != 0:
        addSongs(newPlaylistID, uris)
        uris = ""
    uris += song
    if (idx+1) != len(likedURIs) and (idx+1)%100 != 0:
        uris += ','

addSongs(newPlaylistID, uris)
print('DONE!')
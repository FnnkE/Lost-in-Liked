from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")

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
    url="https://api.spotify.com/v1/users/nerd-e/playlists"
    headers=getAuthHeader(token)
    
    queryURL = url
    
    result = get(queryURL, headers=headers)
    jsonResult = json.loads(result.content)["items"]
    if len(jsonResult )== 0:
        print("No playlists found...")
        return None
    return jsonResult

def getPlaylistSongs(token, playlistID):
    flag = True
    songs = []
    offset = 0
    while flag:
        url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?offset={offset}"
        headers = getAuthHeader(token)
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
        "Authorization": "Bearer TOKEN",
        "Content-Type": "application/json"
        }
    data = {
        "name": "Python 01",
        "description": "All Songs in my Public Playlists",
        "public": "true"
        }
    result = post(url, headers=headers, data=json.dumps(data))
    return json.loads(result.content)['id']

def addSongs(playlistID, uris):
    url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?uris=" + uris
    headers = {
        "Authorization": "Bearer TOKEN",
        "Content-Type": "application/json"
        }
    result = post(url, headers=headers)
    print(result.content)


token = getToken()
result = getPlaylists(token)

playlistMade = False
for playlist in result:
    if playlist["name"] == "Python 01":
        playlistMade = True
        newPlaylistID = playlist['id']

if not playlistMade:
    newPlaylistID = createPlaylist()
playlistIDs  = []
songURIs = []

for idx, playlist in enumerate(result):
    playlistIDs.append(playlist["id"])
    songs = getPlaylistSongs(token, playlist["id"])
    for jdx, song in enumerate(songs):
        newSong = song['track']['uri']
        if newSong not in songURIs:
            songURIs.append(newSong)

uris = ""
for idx, song in enumerate(songURIs):
    if idx%100 == 0 and idx != 0:
        addSongs(newPlaylistID, uris)
        uris = ""
    uris += song
    if (idx+1) != len(songURIs) and (idx+1)%100 != 0:
        uris += ','

addSongs(newPlaylistID, uris)

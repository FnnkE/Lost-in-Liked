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

token = getToken()
result = getPlaylists(token)
playlistIDs  = []
songIDS = []

for idx, playlist in enumerate(result):
    playlistIDs.append(playlist["id"])
    songs = getPlaylistSongs(token, playlist["id"])
    print(len(songs))
    for jdx, song in enumerate(songs):
        newSong = song['track']['id']
        print("newSong")
        if newSong not in songIDS:
            songIDS.append(newSong)


print(songIDS)
print(playlistIDs)

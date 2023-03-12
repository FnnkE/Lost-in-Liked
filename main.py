from dotenv import load_dotenv
import os
import base64
from requests import post, get, delete
import json

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")

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

def getPlaylists(token, username):
    flag = True
    playlists = []
    offset = 0
    while flag:
        url=f"https://api.spotify.com/v1/users/{username}/playlists?limit=50&offset={offset}"
        headers=getAuthHeader(token)
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
        headers = getAuthHeader(token)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)["items"]
        if (len(jsonResult)!=100):
            flag = False
        offset += 100
        songs.extend(jsonResult)
    return songs

def createPlaylist(token, username):
    url = f"https://api.spotify.com/v1/users/{username}/playlists"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
        }
    data = {
        "name": "Lost in Liked™",
        "description": "Being lost is worth the being found | https://github.com/FnnkE/Lost-in-Liked",
        "public": "true"
        }
    result = post(url, headers=headers, data=json.dumps(data))
    return json.loads(result.content)['id']

def addSongs(playlistID, uris, token):
    url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks?uris=" + uris
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
        }
    result = post(url, headers=headers)

def getLikedSongs(token):
    flag = True
    songs = []
    offset = 0
    while flag:
        url=f"https://api.spotify.com/v1/me/tracks?limit=50&offset={offset}"
        headers=getAuthHeader(token)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)["items"]
        if (len(jsonResult)!=50):
            flag = False
        offset += 50
        songs.extend(jsonResult)
        print("Getting Liked Songs: ", offset)
    return songs

def removeSongs(playlistID, token, songs):
    url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
        }
    data = '{"tracks":['
    index = 1
    for song in songs:
        index += 1
        data += '{"uri":"'+ song['track']['uri'] + '"},'
        if index%100 == 0:
            data = data[:-1] + "]}"
            result = delete(url, headers=headers, data=data)
            data = '{"tracks":['
    data = data[:-1] + "]}"
    result = delete(url, headers=headers, data=data)
    return result

#Create user token
token = TOKEN#getToken()
username = 'nerd-e'

#Get user data
liked = getLikedSongs(token)
print('Getting Playlists...')
result = getPlaylists(token, username)

#Playlist setup
playlistMade = False
for playlist in result:
    if playlist["name"] == "Lost in Liked™":
        playlistMade = True
        newPlaylistID = playlist['id']
        print(f'Found Playlist...{newPlaylistID}')
        llSongs = getPlaylistSongs(token, newPlaylistID)
        print(removeSongs(newPlaylistID, token, llSongs))
if not playlistMade:
    newPlaylistID = createPlaylist(token, username)
    print(f'Creating New Playlist... {newPlaylistID}')

#Init vars
playlistIDs  = []
likedURIs = []
songURIs = []

#Get lists of URIs of all songs in each playlists
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

#Get list of URIs of all songs in users "Liked Songs"
for idx, song in enumerate(liked):
    if idx%100 == 0:
        print("Progress: ", idx)
    newSong = song['track']['uri']
    if newSong not in songURIs:
        likedURIs.append(newSong)
print('Liked Songs Put in List...')

#Add songs not in users "Liked Songs" into playlist
uris = ""
for idx, song in enumerate(likedURIs):
    if idx%100 == 0 and idx != 0:
        uris = uris[:-1]
        addSongs(newPlaylistID, uris, token)
        uris = ""
    uris += song + ','
uris = uris[:-1]
addSongs(newPlaylistID, uris, token)
print('DONE!')

from dotenv import load_dotenv
import os
import base64
from requests import post, get, delete
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")


scope = "ugc-image-upload, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, app-remote-control, streaming, playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public, user-follow-modify, user-follow-read, user-read-playback-position, user-top-read, user-read-recently-played, user-library-modify, user-library-read, user-read-email, user-read-private"
auth_manager = SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri='http://lost-in-like.com', scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

def getPlaylists():
    flag = True
    playlists = []
    offset = 0
    while flag:
        playlists = sp.current_user_playlists(limit=50, offset=offset)
        if (len(playlists)!=50):
            flag = False
        offset += 50
        playlists.extend(playlists) #limit output to only items?
        print("Getting playlists: ", offset)
    return playlists

def getPlaylistSongs(playlistID):
    flag = True
    songs = []
    offset = 0
    while flag:
        tracks = sp.playlist_tracks(playlistID, fields=None, limit=100, offset=offset, market=None, additional_types=('track', )) #type and market?
        if (len(tracks)!=100):
            flag = False
        offset += 100
        songs.extend(tracks)
    return songs

def createPlaylist(username):
    result = sp.user_playlist_create(username, '<TEST/> Lost in Liked', public=True, collaborative=False, description='Being lost is worth the being found | https://github.com/FnnkE/Lost-in-Liked')
    #what does result output?
    return result #json.loads(result.content)['id']

def addSongs(playlistID, uris):
    result = sp.playlist_add_items(playlistID, uris, position=None) # None?
    return result # Output?

def getLikedSongs(token):
    flag = True
    songs = []
    offset = 0
    while flag:
        result = sp.current_user_saved_tracks(limit=50, offset=offset, market=None) #market?
        if (len(result)!=50):
            flag = False
        offset += 50
        songs.extend(result)
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
username = 'nerd-e'

#Get user data
liked = getLikedSongs(token)
print('Getting Playlists...')
result = getPlaylists(token, username)

#Playlist setup
playlistMade = False
for playlist in result:
    if playlist["name"] == "</> Lost in Liked":
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
"""
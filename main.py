from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

clientID = os.getenv("CLIENT_ID")
clientSecret = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")

scope = "ugc-image-upload, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, app-remote-control, streaming, playlist-read-private, playlist-read-collaborative, playlist-modify-private, playlist-modify-public, user-follow-modify, user-follow-read, user-read-playback-position, user-top-read, user-read-recently-played, user-library-modify, user-library-read, user-read-email, user-read-private"
#Limit Scope

auth_manager = SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri='http://lost-in-like.com', scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

def getPlaylists():
    flag = True
    playlists = []
    offset = 0
    while flag:
        newPlaylists = sp.current_user_playlists(limit=50, offset=offset)['items']
        if (len(newPlaylists)!=50):
            flag = False
        offset += 50
        playlists.extend(newPlaylists)
        print("Getting playlists: ", offset)
    return playlists

def getPlaylistSongs(playlistID):
    flag = True
    songs = []
    offset = 0
    while flag:
        tracks = sp.playlist_tracks(playlistID, limit=100, offset=offset)['items']
        if (len(tracks)!=100):
            flag = False
        offset += 100
        songs.extend(tracks)
    return songs

def createPlaylist(username):
    return sp.user_playlist_create(username, '</> Lost in Liked', public=True, collaborative=False, description='<LL/> Being lost is worth the being found | https://github.com/FnnkE/Lost-in-Liked')['id']

def addSongs(playlistID, uris):
    sp.playlist_add_items(playlistID, uris)

def getLikedSongs():
    flag = True
    songs = []
    offset = 0
    while flag:
        result = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
        if (len(result)!=50):
            flag = False
        offset += 50
        songs.extend(result)
        print("Getting Liked Songs: ", offset)
    return songs

def removeSongs(playlistID):
    songs = getPlaylistSongs(playlistID=playlistID)
    uris = []
    for idx, song in enumerate(songs):
        if idx%50 == 0 and idx != 0:
            print("Progress: ", idx)
            sp.playlist_remove_all_occurrences_of_items(playlistID, uris)
            uris = []
        newSong = song['track']['uri']
        uris.append(newSong)
    if len(uris) != 0:
        sp.playlist_remove_all_occurrences_of_items(playlistID, uris)

#Get user data
username = sp.current_user()['id']
liked = getLikedSongs()
print('Getting Playlists...')
result = getPlaylists()

#Playlist setup
playlistMade = False
for playlist in result:
    if '&lt;LL&#x2F;&gt;' in playlist['description']:
        playlistMade = True
        newPlaylistID = playlist['id']
        print(f'Found Playlist...{newPlaylistID}')
        removeSongs(newPlaylistID)
if not playlistMade:
    newPlaylistID = createPlaylist(username)
    print(f'Creating New Playlist... {newPlaylistID}')

#Get list of URIs of all songs in users "Liked Songs"
likedURIs = []
songURIs = []
llURIs = []

for idx, song in enumerate(liked):
    if idx%100 == 0:
        print("Progress: ", idx)
    newSong = song['track']['uri']
    likedURIs.append(newSong)
print('Liked Songs Put in List...')

#Get lists of URIs of all songs in each playlists
for idx, playlist in enumerate(result):
    print("Progress: ", idx, " - ", playlist['name'])
    songs = getPlaylistSongs(playlist["id"])
    for idx, song in enumerate(songs):
        try:
            newSong = song['track']['uri']
            if newSong not in songURIs:
                songURIs.append(newSong)
        except:
            print("something went wrong in getting uris... continuing")
print('URIs Obtained...')

for i in likedURIs:
    if i not in songURIs:
        llURIs.append(i)

#Add songs to the Lost in Liked playlist
inRange = True
offset = 0
range = len(llURIs)
while inRange:
    limit = offset + 100
    if limit > range:
        limit = range
    addSongs(newPlaylistID, llURIs[offset:limit])
    print("adding songs", offset, limit)
    offset += 100
    if offset > range:
        inRange = False

print('DONE!')

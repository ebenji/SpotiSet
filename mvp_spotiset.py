import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import spotipy.util as util


def setlist_fm_id(url):
    url_components = url.split('-')

    rough_id = url_components[len(url_components) - 1].split('.')

    setlist_id = rough_id[0]

    return setlist_id

# fill in the spotify api credentials
clientid=""
clientsecret=""
# fill in spotify username
user=""

# put in setlist_fm api key
setlist_fm_token=""
# this header should contain YOUR unique token
headers = {'Accept': 'application/json', 'x-api-key': setlist_fm_token}


# parse out the code from the end (which is the setlistId)
url=input("> ")

setlistid=setlist_fm_id(url)
# issue this get request
request_syntax = 'https://api.setlist.fm/rest/1.0/setlist/' + setlistid
data = requests.get(request_syntax, headers = headers)

# this is the data here (and it must be decoded from a raw byte string)

data1=json.loads(data.content)

artist=data1['artist']['name']

songs = []
for _set in data1['sets']['set']:
    for song in _set['song']:
        songs.append(song['name'])

for song in range(len(songs)):
    a=songs[song]
    songs[song]=a+' '+'"'+artist+'"'

token=util.prompt_for_user_token(user,"playlist-modify-private",client_id=clientid,client_secret=clientsecret,redirect_uri='http://localhost:8888/callback')
sp=spotipy.Spotify(auth=token)
ids=[]
for s in range(len(songs)):
    response=sp.search(songs[s],type="track,artist", limit=1,market="US")
    id=response['tracks']['items'][0]['id']
    ids.append(id)

# create blank playlist
play=sp.user_playlist_create(user, "Setlist", public=False)
# put in the playlist id of the playlist that was created, can be found on spotify app
playlistid=""

#add tracks
sp.user_playlist_add_tracks(user, playlistid, ids, position=None)




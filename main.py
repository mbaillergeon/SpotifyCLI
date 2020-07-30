import spotipy
import spotipy.util as util
import os
import urllib.request
from dotenv import load_dotenv

from playback.playback import gonextsong
load_dotenv()

username = os.environ.get('USERNAME')
scope = 'user-modify-playback-state user-read-playback-state user-top-read app-remote-control'
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = os.environ.get('REDIRECT_URI')

token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
print(client_id)

def startsong():
    sp.start_playback()

def pausesong():
    sp.pause_playback()

if __name__ == "__main__":
    
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        print('yes')
    else:
        print("Can't get token for", username)

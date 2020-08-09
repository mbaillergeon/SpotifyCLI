import spotipy
import spotipy.util as util
import os
import random
import urllib.request
from dotenv import load_dotenv
from playback.playback import gonextsong
import click
load_dotenv()

username = os.environ.get('USERNAME')
scope = 'user-modify-playback-state user-read-playback-state user-top-read app-remote-control'
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
redirect_uri = os.environ.get('REDIRECT_URI')

token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)

@click.group()
def cli():
    pass

@cli.command(name='next')
def gonextsong():
    #skips to the next song
    print('----------')
    print('Playing Next Song')
    sp.next_track()
    # displaycurrentsong()

@cli.command(name='bang')
def bangers():
    #fuction to pass the uri list to the add to queue function
    addtoqueue(generatetoplist())

def toptracks():
    #prints out a list of the all time top tracks for a user
    results = sp.current_user_top_tracks(time_range='long_term')
    for i, item in enumerate(results['items']):
        print(i, item['name'], item['uri'])

def generatetoplist():
    #looks through the user's top tracks, gets the uri for the songs, shuffles then, returns five of them
    trackurilist = []
    results = sp.current_user_top_tracks(limit = 50, time_range='long_term')
    for item in results['items']:
        trackurilist.append(item['uri'])
    random.shuffle(trackurilist)
    return trackurilist[:5]

def addtoqueue(urilist):
    #adds a list of uri's to the user's queue
    smallurilist = urilist
    print('Adding Songs to Queue')
    for uri in smallurilist:
        sp.add_to_queue(uri)
    print('Done!')

@cli.command(name='playing')
def displaycurrentsong():
    #gets the url and info from getcurrentsong, updates the label 

    if getcurrentsong():
        songimageurl, songinfo = getcurrentsong()
        click.echo(f'----------\n{songinfo}\n----------')
    else:
        return None

def getcurrentsong():
    #gets the current song playing on spotify and returns a tuble of the allbum URL and a formatted title string 
    results = sp.currently_playing(market = 'US')
    if results:
        songinfoformatted  =  '\n' + results['item']['name'] + ' by ' + results['item']['album']['artists'][0]['name'] + '\n'
        return results['item']['album']['images'][1]['url'], songinfoformatted
    else:
        return None
        
@cli.command(name='back')
def backsong():
    sp.previous_track()

@cli.command(name='repeat')
def repeatstate(state):
    #state: track, context, off
    statedict = {0:'track',1:'context',2:'off'}
    stateword = statedict[state]
    print(stateword)
    sp.repeat(stateword)

@cli.command(name='shuffle')
def shuffle():
    if shuffling == False:
        print('Shuffling')
        sp.shuffle(True)
        shuffling = True
    else:
        print('Stop Shuffling')
        sp.shuffle(False)
        shuffling = False
    #state: True, False


@cli.command(name='vol')
def volumechange(value):
    sp.volume(23)

@cli.command(name='play')
def startsong():
    sp.start_playback()

@cli.command(name='pause')
def pausesong():
    sp.pause_playback()

if __name__ == "__main__":
    
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
    else:
        print("Can't get token for", username)

    cli()
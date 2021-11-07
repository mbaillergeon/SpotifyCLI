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
scope = 'user-modify-playback-state user-read-playback-state user-top-read app-remote-control playlist-read-private'
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
    print('NEXT')
    sp.next_track()
    displaycurrentsong()
    # displaycurrentsong()

@cli.command(name='bang')
@click.argument('time')
def bangers(time):
    #fuction to pass the uri list to the add to queue function
    addtoqueue(generatetoplist(time))

def toptracks(time):
    #prints out a list of the all time top tracks for a user
    results = sp.current_user_top_tracks('long_term')
    for i, item in enumerate(results['items']):
        print(i, item['name'], item['uri'])

def generatetoplist(time):
    #looks through the user's top tracks, gets the uri for the songs, shuffles then, returns five of them
    trackurilist = []

    if time == 'short':
        time_range = 'short_term'
    elif time == 'mid':
        time_range = 'medium_term'
    else:
        time_range = 'long_term'

    results = sp.current_user_top_tracks(limit = 50, time_range=time_range)
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
def displaycurrentplaying():
    displaycurrentsong()

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

@cli.command(name='playlistlist')
def getplaylists():
    results = sp.current_user_playlists()
    for number, playlist in enumerate(results['items']):
        # print(playlist["uri"])
        print (f'Number: {number} Name: {playlist["name"]}')

@cli.command(name='playplaylist')
@click.argument('playlistnumber')
def playplaylist_command(playlistnumber):
    return playplaylist(playlistnumber)

def playplaylist(playlistnumber):
    playlistnames = {}
    results = sp.current_user_playlists()
    for number, playlist in enumerate(results["items"]):
        playlistnames[number] = playlist["uri"]

    sp.start_playback(None, playlistnames[int(playlistnumber)])

    playlisttracks(playlistnames[int(playlistnumber)])

def playlisttracks(playlistid):
    # print(sp.playlist_tracks(playlistid))
    results = sp.playlist_tracks(playlistid)
    for track in results['items'][:10]:
        print(track['track']['name'])


@cli.command(name='back')
def backsong():
    sp.previous_track()
    displaycurrentsong()

@cli.command(name='repeat')
def repeatstate(state):
    #state: track, context, off
    statedict = {0:'track',1:'context',2:'off'}
    stateword = statedict[state]
    print(stateword)
    sp.repeat(stateword)

@cli.command(name='shuffle')
@click.argument('shuffleswitch')
def shuffle(shuffleswitch):
    print(shuffleswitch)
    if shuffleswitch == "on":
        sp.shuffle(True)
        print('SHUFFLING ON')
    else:
        sp.shuffle(False)
        print('SHUFFLING OFF')
    # if shuffling == False:
    #     print('Shuffling')
    #     sp.shuffle(True)
    #     shuffling = True
    # else:
    #     print('Stop Shuffling')
    #     sp.shuffle(False)
        # shuffling = False
    #state: True, False


@cli.command(name='vol')
@click.argument('volumelevel')
def volumechange(volumelevel):
    sp.volume(int(volumelevel))
    print(f'Volume Changed to: {volumelevel}')

@cli.command(name='play')
def startsong():
    sp.start_playback()
    displaycurrentsong()

@cli.command(name='pause')
def pausesong():
    sp.pause_playback()

@cli.command(name='study')
def studytime():
    print("in the studytime")
    return playplaylist(7)



if __name__ == "__main__":
    
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
    else:
        print("Can't get token for", username)

    cli()

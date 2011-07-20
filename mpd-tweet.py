App_Name = "MPD-Tweet"
Consumer_key = "n9gj3P5Ug3bhnNNF4p3ow"
Consumer_secret = "7FIAaTZQAFcNboWXVUUlTffxzbDVEY7iwXw67fyd7Q"
Config_file="config"
MPDHost = 'localhost'
MPDPort = '6600'

from lib.oauth_dance import oauth_dance
from lib.oauthtwitter import OAuthApi
from lib.oauth import read_token_file
from mpd import MPDClient, CommandError, MPDError
from socket import error as SocketError

class Tweet:
    def __init__(self):
        self.generate_config()
        api = self.get_twitter_access()
        mpdclient = self.connect_to_mpd()
        currentSong =  mpdclient.currentsong()
        self.tweet_now_playing(currentSong, api)
        
    def generate_config(self):
        try:
            f = open(Config_file)
        except IOError:
            oauth_dance(App_Name, Consumer_key, Consumer_secret, Config_file)
    
    def get_twitter_access(self):
        token = read_token_file(Config_file)
        api = OAuthApi(Consumer_key, Consumer_secret, token[0], token[1])
        return api
        
    def connect_to_mpd(self):
        client=MPDClient()
        try:
            client.connect(MPDHost, MPDPort)
            return client
        except SocketError:
            print "Unable to connect to MPD on %s on port %s" % (MPDHost, MPDPort)
        
    def tweet_now_playing(self, currentSong, api):
        currentSong['album'] =""
        status = ("Listening to %s by %s #nowplaying" ) % (currentSong['title'], currentSong['artist'])
        print status 
        api.UpdateStatus(status)
        
            
    
if __name__ == "__main__":
    Tweet = Tweet()

from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API

import json
import tweet_auth

# Authenticator class to handle authenticaiton and connection to Twitter API
class Authenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(tweet_auth.consumer_key, tweet_auth.consumer_secret)
        auth.set_access_token(tweet_auth.access_token, tweet_auth.access_token_secret)
        return auth

# define a Tweet listener object
class BasicStreamListener(StreamListener):
    """
    Class for basic stream listening
    """
    def __init__(self, tweets_holder_file, api=None):
        super(BasicStreamListener, self).__init__()
        self.file_name = tweets_holder_file
        # initiate tweets counter
        self.num_tweets = 0
        # creates a file
        #self.file = open("tweets.txt", "w")

    def on_data(self, data):
        #tweet = data
        #tweet = data._json
        with open(self.file_name, "a") as file:
            #file.write(json.dumps(tweet) + '\n')
            file.write(data)
        self.num_tweets += 1
        if self.num_tweets < 10:
            return True
        else:
            return False
        self.file.close()
        #try:
        #    with open(self.tweets_holder_file, 'a') as tf:
        #        tf.write(data)
        #    return True
        #except BaseException as err:
        #    print("Error on_data: %s" % str(err))
        #return True

    def on_error(self, status):
        if status == 420:
            # return false on_data method incase rate limit occurs (b4 API kicks you)
            return False
        print(status)

###
class TagStreamer():
    """
    Class for authentication, connect to API and filter input tags
    """
    def __init__(self):
        self.twitter_authenticator = Authenticator()

    def stream_tweets(self, tweets_holder_file, hash_tag_list):
        # initialise a StreamListener object
        peppa = BasicStreamListener(tweets_holder_file)
        # configure authentication
        auth = self.twitter_authenticator.authenticate_twitter_app()
        # create Stream object and include auth
        stream = Stream(auth, peppa)
        # Filter Streams to capture keywords
        stream.filter(track=hash_tag_list)

if __name__ == "__main__":

    hash_tag_list = ["genome", "genomic test", "gene sequencing"]
    tweets_holder_file = "tweets2.txt"

    tag_streamer = TagStreamer()
    tag_streamer.stream_tweets(tweets_holder_file, hash_tag_list)

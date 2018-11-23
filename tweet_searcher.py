from TwitterSearch import *
import numpy as np
import json

import tweet_auth

#retro_tweets = []

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['genomic test']) # let's define all words we would like to have a look for
    #tso.set_language('en')
    tso.set_include_entities(False) # and don't give us all those entity information

    # TwitterSearch object taking authentication credentials
    searcher = TwitterSearch(
        consumer_key = tweet_auth.consumer_key,
        consumer_secret = tweet_auth.consumer_secret,
        access_token = tweet_auth.access_token,
        access_token_secret = tweet_auth.access_token_secret
     )

     # this is where the fun actually starts :)
    with open("retro_tweets.txt", "a") as file:
        for tweet in searcher.search_tweets_iterable(tso):
            #print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
            file.write(json.dumps(tweet) + '\n')

    #with open("retro_tweets.txt", "w") as file:
        #file.write(str(retro_tweets))

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)

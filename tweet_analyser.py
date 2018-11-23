import json
import pandas as pd
import numpy as np

###
class TweetAnalyser():
    """
    Should extract text into df
    """
    def into_df(self, tweets_path):
        raw_tweets = []
        with open(tweets_path, "r") as file:
            for entry in file:
                tweet = json.loads(entry)
                raw_tweets.append(tweet)
        print("This is the list of retrievable features: \n\n%s\n" %(tweet.keys()))
        # turn list "raw_tweets" into a data frame, maybe I can do this straight from JSON dict
        df = pd.DataFrame(data=[twt['text'] for twt in raw_tweets], columns=['Tweets'])
        df["lang"] = np.array([twt["lang"] for twt in raw_tweets])
        df["geo"] = np.array([twt["geo"] for twt in raw_tweets])
        df["source"] = np.array([twt["source"] for twt in raw_tweets])
        df["created_at"] = np.array([twt["created_at"] for twt in raw_tweets])

        print("Your selected DataFrame features: \n\n%s\n" %(np.array(df.columns)))
        return df

if __name__ == "__main__":

    tweet_analyser = TweetAnalyser()
    #df = tweet_analyser.into_df("tweets2.txt")
    df = tweet_analyser.into_df("retro_tweets.txt")

    #print(df.iloc[5])
    #print(raw_tweets)
    #print(df.head())
    print(df.iloc[:,0])

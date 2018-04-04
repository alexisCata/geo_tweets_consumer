from json import loads

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Variables that contains the user credentials to access Twitter API
access_token = "979004915753332737-eSMw8L38DKgPfbec8PCqrRUdAv1hgbz"
access_token_secret = "nKmB1OaDuFKYQYTwQMYfGxLh99ikmXfcPJr4xSvzJTbtF"
consumer_key = "NpyZzwURobp91NapSvDrIgALv"
consumer_secret = "UMVUMDQktTuFILpCeG5mxp9oEBrTYFmWN95Ytl3aV3RP5hjt7i"

ERROR_CODES = {304: "Not Modified",
               400: "Bad Request",
               401: "Unauthorized",
               403: "Forbidden",
               404: "Not Found",
               406: "Not Acceptable",
               410: "Gone",
               420: "Enhance Your Calm",
               422: "Unprocessable Entity",
               429: "Too Many Requests",
               500: "Internal Server Error",
               502: "Bad Gateway",
               503: "Service Unavailable",
               504: "Gateway timeout"}


class CustomListener(StreamListener):
    """
    Listener class for Twitter streaming API
    Receive a mongo database instance to store de tweets
    """

    def __init__(self, mongo_db):
        self.db = mongo_db
        super().__init__()

    def on_data(self, data):
        tweet = loads(data)
        if "coordinates" in tweet and tweet["coordinates"]:
            self.db.tweets.replace_one({}, tweet, upsert=True)
        return True

    def on_error(self, status):
        try:
            print(ERROR_CODES[status])
        except Exception as e:
            print(e)


def consume_geo_tweets(db):
    """
    Start a Twitter streaming API listener and consume geo tweets
    Receives a mongodb instance as parameter
    """

    # Handles Twitter auth and the connection to Twitter Streaming API
    listener = CustomListener(db)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    # Consume geo tweets
    stream.filter(locations=[-180, -90, 180, 90], async=False)

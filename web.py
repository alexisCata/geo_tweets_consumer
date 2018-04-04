import socket
from decimal import Decimal
from json import dumps
from threading import Thread

from flask import Flask, render_template, request
from pymongo import MongoClient

from twitter import consume_geo_tweets

app = Flask(__name__)

try:
    socket.gethostbyname("db")
    client = MongoClient("db")
except:
    client = MongoClient()
db = client.tweets


@app.route('/')
def index():
    t = Thread(target=consume_geo_tweets, args=(db,))
    t.start()

    return render_template('index.html')


@app.route('/tweets')
def get_tweets():
    coords = (request.args.get("coord1", None), request.args.get("coord2", None))

    tweets = []

    c_tweets = db.tweets.find({})

    stored_tweets = [{"coordinates": t["geo"]["coordinates"],
                      "user": t["user"]["name"],
                      "user_id": t["user"]["id_str"],
                      "tweet_id": t["id_str"],
                      "created_at": t["created_at"],
                      "text": t["text"]} for t in c_tweets]

    ids = [t["_id"] for t in c_tweets]

    db.tweets.remove({"_id": {"$in": ids}})

    if not coords[0] and not coords[1]:
        tweets = stored_tweets
    else:
        for tweet in stored_tweets:
            if coords[0] and (Decimal(coords[0]) - 2 <= Decimal(tweet["coords"][0]) <= Decimal(
                    coords[0]) + 2) or \
                            coords[1] and (
                                        Decimal(coords[1]) - 2 <= Decimal(tweet["coords"][1]) <= Decimal(
                                coords[1]) + 2):
                tweets.append(tweet)

    tweets.reverse()

    return dumps(tweets, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

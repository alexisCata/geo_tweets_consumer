# Geo tweets #

Web application that consumes geo tweets using Twitter Streaming API, and shows tweets from all around the world allowing filtering by coordinates, also placing in a map the coordinates of the tweets.

Using Python for the backend with Flask, Tweepy and Pymongo for the backend and JQuery and Google Maps Api for the frontend.

## Files explanation
##### - twitter.py
Using tweepy and pymongo.

**CustomListener** is a custom class child of **StreamListener** to consume geo tweets and handle received streaming data to save it into a MongoDB database.

**consume_geo_tweets** is function that starts the consumer and filters geo tweets.

##### - web.py

Using Flask framework and pymongo.

I set up a web that starts a **Thread** that calls the function **consume_geo_tweets** to start consuming geo tweets and storing them in db.

With Ajax I make a request each second to retrieve the tweets from db and show them. (I decide to delete the tweets after retrieve them from DB)

You can filter to show only tweets in certain coordinates (it works with one or two coordinate points). 

The tweets coodinates will be shown in the map.

## How to use

There are two options to use it.
#### 1.
The first option needs a MongoDB database running on localhost

```
pip install virtualenv
```
```
virtualenv venv -p /usr/bin/python3
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
python web.py
```

Then, in a browser http://127.0.0.1:5000

#### 2.
For the second option you will need only Docker installed.

```
docker-compose up
```
It will create two docker containers. One with MongoDB and the other with the WebApp.

Then, in a browser http://127.0.0.1:5000

##### Notes
The Google Maps API could fail loading with Adblock enabled throwing a JS error. Also I have read about some problems with Firefox with the new Google Maps API v3 (Im using 3.32.6)

## Dependencies
    
[Flask](http://flask.pocoo.org/)

[Tweepy](http://www.tweepy.org/)

[PyMongo](https://api.mongodb.com/python/current/)

[MongoDB](https://www.mongodb.com)

or 

[Docker](https://www.docker.com/)

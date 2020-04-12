# database API - http://www.omdbapi.com/
# now we're getting the poster URL back from omdb, just need to download it and reply with a tweet
# https://stackoverflow.com/questions/31748444/how-to-update-twitter-status-with-image-using-image-url-in-tweepy
# https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python_part_two-posting_with_photos/
# create a function with api.mediaA_upload and use the returl value in update_status(status=tweet, media_ids=[media.media_id])
# what is a media object

# poster is now downloaded, simply reply to the parent tweet with the poster

import tweepy
import os
import requests
import datetime

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
key = os.getenv("KEY")
secret = os.getenv("SECRET")
omdb_api = os.getenv("OMDB_API")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key,secret)

try:
    api = tweepy.API(auth)
except tweepy.TweepError as e:
    print(e)

class MySTreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_text = tweetTextAction(status.text)
        print(f"Searching omdb for {tweet_text}")
        poster = omdb_query(tweet_text)
        print(f"Poster URL > {poster}")
        f = download_poster(poster)
        print(f"Downloaded poster for {tweet_text}")
        media = api.media_upload(f)
        api.update_status(status=":)", media_ids=[media.media_id])
        print("updated status")
        
    
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

def tweetTextAction(tweet):
    x = tweet.split()
    y = str.join(' ', (x[1:]))
    return y


def omdb_query(movie_name):
    payload = {"t" : movie_name}
    url = "http://www.omdbapi.com/?apikey=" + omdb_api
    r = requests.get(url, params=payload)
    resp = r.json()
    return resp['Poster'] 

def download_poster(image_url):
    time = datetime.datetime.now()
    filename = time.strftime("%H%M") + ".jpg"
    filename = "100.jpg"
    f = open(filename, 'wb')
    f.write(requests.get(image_url).content)
    f.close()
    return filename

listener= MySTreamListener()
my_stream = tweepy.Stream(auth = api.auth, listener=listener)

my_stream.filter(track=['@bulundindia1337'])

import tweepy
from dotenv import load_dotenv
import os
# load data from .env file
load_dotenv()
# get env vars from .env file, assign to tweepy client
client = tweepy.Client(consumer_key=os.getenv('CONSUMER_KEY'),
                       consumer_secret=os.getenv('CONSUMER_SECRET'),
                       access_token=os.getenv('ACCESS_TOKEN'),
                       access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'))
# create tweet with token credentials
text_to_tweet = ""
# response = client.create_tweet(text='testing testing 1,2,3 its me ralph lawler ')
def send_tweet(tweet_text):
    '''
    creates a plaintext tweet from @lawlers_laws account.  content of tweet is passed in as "tweet_text" var
    '''
    tweet_response = client.create_tweet(text=tweet_text)
# print response from twitter to console, verifying that the tweet was sent
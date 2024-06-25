from flask import Flask, render_template
import requests
import tweepy
import praw

app = Flask(__name__)

def get_price_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=1"
    response = requests.get(url)
    data = response.json()
    return data

def get_tweets(hashtag):
    auth = tweepy.OAuthHandler("API_KEY", "API_SECRET")
    auth.set_access_token("ACCESS_TOKEN", "ACCESS_SECRET")
    api = tweepy.API(auth)
    tweets = api.search(q=hashtag, count=100)
    return tweets

def get_reddit_posts(subreddit):
    reddit = praw.Reddit(client_id='CLIENT_ID', 
                         client_secret='CLIENT_SECRET', 
                         user_agent='USER_AGENT')
    posts = reddit.subreddit(subreddit).hot(limit=10)
    return posts

@app.route('/')
def home():
    price_data = get_price_data('bitcoin')
    tweets = get_tweets('#Bitcoin')
    posts = get_reddit_posts('cryptocurrency')
    return render_template('index.html', price_data=price_data, tweets=tweets, posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

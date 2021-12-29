from flask import Flask, render_template, request

from twitter_auth import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

import tweepy as tp
import tweets as t


# this section prepares the connection with twitter
auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tp.API(auth)



app = Flask(__name__)

# declaring that this has 2 methods: get, post
@app.route('/', methods=['GET', 'POST'])
def process_query():
    if request.method == 'POST':
        query = request.form['query']

        # collecting the tweets from twitter
        max_tweets = 400
        tweets_JSON = [status for status in tp.Cursor(api.search, q=query+' -filter:retweets', lang='en', tweet_mode='extended').items(max_tweets)]
        cleaned_tweets = t.clean_and_save_tweets(tweets_JSON)



        return render_template('results.html', tweets=cleaned_tweets)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()

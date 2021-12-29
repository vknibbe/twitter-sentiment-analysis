# Functions to clean and save tweets collected by Flask app

import re

def clean_tweet(tweet):
    """
    Function to clean each individual tweet using Regular Expressions
    """
    # remove @ mentions
    tweet = re.sub(r'@[A-Za-z0-9_]+', '', tweet)

    # remove RT sign in the beginning of the tweet
    tweet = re.sub(r'‚Ä¶', '', tweet)

    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', '', tweet)

    # remove https (https://urlregex.com/)
    tweet = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)

    # remove hashtags
    tweet = re.sub(r'#[A-Za-z0-9_]+', '', tweet)

    # replacing new lines with 3 spaces, so each line represents one tweet
    tweet = re.sub(r'\r?\n?\r?\n?', '', tweet)

    # replace ampersand with and
    tweet = re.sub(r'&amp;', 'and', tweet)

    # Emoji patterns
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U00002192"
                               "]+", flags=re.UNICODE)
    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    return tweet


def clean_and_save_tweets(tweets):
    """
    Function to process the tweets gathered by the flask app, including:
        - check if the tweet is a retweet (and discard it if so),
        - clean the tweet,
        - write the cleaned tweet and associated functions to file
        - return a list of all the cleaned tweets
    """

    # open the file to store the tweets and other features
    with open('thunberg_full_tweets.txt', 'w', encoding='utf-8') as file:

        # list to store all the cleaned tweets
        cleaned_list = []

        # for each tweet
        for tweet in tweets:

            # discard tweet if it has the retweeted attribute
            # (this ensures no duplicated tweets and removes difficulties in accessing the full tweet text)
            if hasattr(tweet, 'retweeted_status'):
                continue

            # extract full tweet text and clean it
            tweet_uncleaned = tweet.full_text
            tweet_cleaned = clean_tweet(tweet_uncleaned)

            # append cleaned tweet to list
            cleaned_list.append(tweet_cleaned)

            # write other tweet details to file
            all_details = tweet_cleaned + ';' + str(tweet.user.location) + ';' + str(tweet.user.followers_count) + ';' \
                + str(tweet.user.friends_count) + ';' + str(tweet.user.following) + ';' \
                + str(tweet.coordinates) + ';' + str(tweet.place) + ';' + str(tweet.retweet_count) + ';' \
                + str(tweet.favorite_count)
            file.write(all_details + '\n')

    return cleaned_list

# Function to run VADER Sentiment Intensity Analyzer.
# Labelling is based on the Compound score, which varies from 1 to -1.
#       - positive: 1 <= compound < 0.25
#       - neutral: 0.25 <= compound < (-0.25)
#       - negative: -0.25 <= compound <= -1
# Prints accuracy and confusion matrix

# import nltk
# nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score


def sentiment_analyzer_scores(tweet_list, y):
    vader_sentiments = []
    analyser = SentimentIntensityAnalyzer()
    x = -1

    # loop through each tweet to predict sentiment
    for tweet in tweet_list:
        x = x+1

        # extract compound score from VADER
        compound_score = analyser.polarity_scores(tweet)['compound']

        # add sentiment to VADER sentiments list, based on compound score
        if compound_score <= -0.1:
            vader_sentiments.append('negative')
        elif compound_score <= 0.32:
            vader_sentiments.append('neutral')
        else:
            vader_sentiments.append('positive')

    # accuracy score
    print('Results from VADER Sentiment Prediction')
    print('Accuracy score:')
    acc = accuracy_score(y, vader_sentiments)
    print(acc)

    # confusion matrix
    cm = pd.DataFrame(confusion_matrix(y, vader_sentiments))
    print('Confusion matrix:')
    print(cm)
    print()

    return vader_sentiments


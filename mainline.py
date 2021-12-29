# Mainline program
"""
Mainline Program
- Creates Classifier Model
    - Reads in data
    - Adds extra text features
    - Creates x, y, test/train split
    - Builds classifier
    - Checks results
- Compares results
    - from testing against another domain - Vegemite tweets
    - with results from VADER
    - with VADER results for Vegemite tweets

"""
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import pandas as pd
import re

import pipeline as pipe

import vader_sentiments as vdr

#################### FEATURE ENGINEERING FUNCTION ###############################


def add_text_features(df):
    """
    Function for feature engineering. Adds three new features to the dataset:
        - processed: with the text in lowercase and punctuation removed
        - length: the total character length of the tweet
        - words: the number of words seperated by spaces
    """
    # process tweet by lowering and removing punctuation
    df['processed'] = df['text'].apply(lambda x: re.sub(r'[^\w\s]', '', x.lower()))

    # add total length of tweet
    df['length'] = df['processed'].apply(lambda x: len(x))

    # add number of words
    df['words'] = df['processed'].apply(lambda x: len(x.split(' ')))

    return df


#################### CREATING CLASSIFIER MODEL ###############################

# Read data into DataFrame and add column names
col_names = ['text', 'location', 'followers', 'friends', 'following', 'coordinates', 'place', 'retweets', 'favorites', 'labels']
data = pd.read_csv('thunberg_full_labelled.txt', sep=';', header=None, names=col_names, encoding='utf-8')

# drop data columns which are empty
data.drop('following', axis=1, inplace=True)
data.drop('coordinates', axis=1, inplace=True)
data.drop('place', axis=1, inplace=True)
data.drop('location', axis=1, inplace=True)

# add text features to DataFrame
data = add_text_features(data)

# Check data
# print(data.head())
# print(data.isnull().sum())
# print(data.describe())

# create x and y
y = data['labels']
x = data.drop(['labels', 'text'], axis=1)

# test train split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=32, stratify=y)

# # check datasets are balanced after splitting
print(y.value_counts()/len(y))
# print(y_train.value_counts()/len(y_train))

# build classifier
classifier = pipe.pipeline.fit(x_train, y_train)

# check results
# - accuracy
print(" - THUNBERG TWEETS - ")
print("Results from SVM Classifier")
print('Accuracy: ', pipe.pipeline.score(x_test, y_test))

# - confusion matrix
y_pred = pipe.pipeline.predict(x_test)
cm = pd.DataFrame(confusion_matrix(y_test, y_pred))
print('Confusion matrix:')
print(cm)
print()

#################### TESTING AND COMPARING RESULTS ###############################

# Accuracy of VADER sentiment prediction
new_y = vdr.sentiment_analyzer_scores(x_test['processed'], y_test)

#### Testing classifier model with data from another domain - 'Vegemite' tweets

# Read data into DataFrame and add column names
col_names = ['text', 'location', 'followers', 'friends', 'following', 'coordinates', 'place', 'retweets', 'favorites', 'labels']
data = pd.read_csv('veg_full_labelled.txt', sep=';', header=None, names=col_names, encoding='utf-8')

# drop data columns which are empty
data.drop('following', axis=1, inplace=True)
data.drop('coordinates', axis=1, inplace=True)
data.drop('place', axis=1, inplace=True)
data.drop('location', axis=1, inplace=True)

# add text features to DataFrame
data = add_text_features(data)

# Check data
# print(data.head())
# print(data.isnull().sum())
# print(data.describe())

# create x and y
y = data['labels']
x = data.drop(['labels', 'text'], axis=1)

# test train split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=32, stratify=y)

# check results
# - accuracy
print(" - VEGEMITE TWEETS - ")
print("Results from Thunberg-trained SVM Classifier")
print('Accuracy: ', pipe.pipeline.score(x_test, y_test))

# - confusion matrix
y_pred = pipe.pipeline.predict(x_test)
cm = pd.DataFrame(confusion_matrix(y_test, y_pred))
print('Confusion matrix:')
print(cm)
print()

# Accuracy of VADER sentiment prediction on Vegemite tweets
vdr.sentiment_analyzer_scores(x_test['processed'], y_test)

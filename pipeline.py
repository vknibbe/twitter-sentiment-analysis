# Methods, classes and pipelines for creating the classifier model

# imports for vectorizing
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# imports for pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline

# imports for creating model
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

#################### PREPARATION FOR TOKENIZING###############################

def tokenize(text):
    """
    Function to tokenize text (for before inputting into Vectorizer)
    """
    stemmer = PorterStemmer()
    return [stemmer.stem(w) for w in word_tokenize(text)]



stp_words = stopwords.words('english')
added_words = ['Greta', 'Thunberg', 'greta', 'thunberg', 'Vegemite', 'vegemite']
for word in added_words:
    stp_words.append(word)

#################### CLASSES FOR COLUMN SELECTORS ###############################

class TextSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on text columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]


class NumberSelector(BaseEstimator, TransformerMixin):
    """
    Transformer to select a single column from the data frame to perform additional transformations on
    Use on numeric columns in the data
    """
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[[self.key]]


#################### PIPELINE FOR EACH FEATURE ###############################

# Pipeline to vectorize processed tweet text
processed_text = Pipeline([
                ('selector', TextSelector(key='processed')),
                ('vectorizer', TfidfVectorizer(stop_words=stp_words, tokenizer=tokenize))
            ])

# Pipeline to scale followers feature
followers = Pipeline([
                ('selector', NumberSelector(key='followers')),
                ('scaler', MinMaxScaler(feature_range=(-1, 1)))
            ])

# Pipeline to scale friends feature
friends = Pipeline([
                ('selector', NumberSelector(key='friends')),
                ('scaler', MinMaxScaler(feature_range=(-1, 1)))
            ])

# Pipeline to scale retweets feature
retweets = Pipeline([
                ('selector', NumberSelector(key='retweets')),
                ('scaler', MinMaxScaler(feature_range=(-1, 1)))
            ])

# Pipeline to scale favorites feature
favorites = Pipeline([
                ('selector', NumberSelector(key='favorites')),
                ('scaler', MinMaxScaler(feature_range=(-1, 1)))
            ])

# Pipeline to scale length feature
length = Pipeline([
                ('selector', NumberSelector(key='length')),
                ('scaler', MinMaxScaler(feature_range=(-1, 1)))
            ])

# Pipeline to scale words feature
words = Pipeline([
                ('selector', NumberSelector(key='words')),
                ('scaler', MinMaxScaler(feature_range=(-1, 1)))
            ])


#################### FINAL PIPELINE INCLUDING FEATURE UNION OF ABOVE PIPELINES ###############################

pipeline = Pipeline([
    ('features', FeatureUnion([('text', processed_text),
                        ('followers', followers),
                        ('friends', friends),
                        ('retweets', retweets),
                        ('favorites', favorites),
                        ('length', length),
                        ('words', words)])),
    ('classifier', SVC(kernel='poly', degree=2, C=3))])


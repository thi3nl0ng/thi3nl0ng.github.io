import re
import json
import time
import pickle
import numpy as np
import pandas as pd

from nltk.corpus import stopwords

from string import punctuation
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold, KFold, train_test_split

stopwords_1 = set(stopwords.words('english'))
stopwords_2 = set([word.rstrip() for word in open('stopwords.txt', 'r')])
stopwords = list(set(stopwords_1 | stopwords_2))

def text_preprocessor(text):
    text = text.rstrip()
    # remove punctuation
    text = ''.join([char for char in text if char not in punctuation])
    
    words = [w.strip() for w in text.split()]
    return ' '.join(words)


class TweetClassifier(object):

    def __init__(self, data_path, label_field='label', text_field='text', \
                 model=None, pipeline=None, test_params=None):

        if model is None:
            self.model = MultinomialNB()
        else:
            self.model = model
        
        self.data_path = data_path
        self.label_field = label_field
        self.text_field = text_field
        self.data = self.load_data()

       
        if pipeline is None:
            self.pipeline = Pipeline([
                                        ('vectorizer',  CountVectorizer(
                                                            stop_words=stopwords,
                                                            tokenizer=tokenizeRawTweetText,
                                                            )),
                                        ('tfidf', TfidfTransformer() ),
                                        ('classifier',  self.model)
                                    ])
        else:
            self.pipeline = pipeline
    
    def load_data(self):	
        listTweets = []
        for acc in self.data_path:
            tweets = pd.read_csv(acc + '_tweets.csv')			
            tweets['label'] = acc
            #tweets['text'] = tokenizeRawTweetText(tweets['text'])
            listTweets.append(tweets)
        tweets = pd.concat(listTweets, axis = 0, ignore_index = True)
        tweets_df = pd.DataFrame(tweets)
        return tweets_df

    def train(self):
        train_text = self.data[self.text_field].values
        train_y = self.data[self.label_field].values
        self.pipeline.fit(train_text, train_y)

    def cross_validate(self, n_folds=5, pos_label=1):       
        k_fold = KFold(n_splits=n_folds,shuffle=True)      
        X = np.arange(0,len(self.data))
		
        scores = []
        confusion = np.array([[0, 0], [0, 0]])       
        for train_indices, test_indices in k_fold.split(X):
           
            train_text = self.data.iloc[train_indices][self.text_field].values
            train_y = self.data.iloc[train_indices][self.label_field].values
            test_text = self.data.iloc[test_indices][self.text_field].values
            test_y = self.data.iloc[test_indices][self.label_field].values           
            # self.train(train_text, train_y)
            # predictions = self.predict(test_text)
            self.pipeline.fit(train_text, train_y)
            predictions = self.pipeline.predict(test_text)

            confusion += confusion_matrix(test_y, predictions)
            score = f1_score(test_y, predictions, pos_label=pos_label)
            scores.append(score)

        print('Total instances classified:', len(self.data))
        print('Score:', sum(scores)/len(scores))
        print('Confusion matrix:')
        print(confusion)

    def save_model(self, _folder):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = 'model_'+timestr+'.pkl'
        with open(_folder+'/'+filename, 'wb') as fout:
            pickle.dump(self.pipeline, fout)
        return filename

    def load_model(self, path):
        self.pipeline = pickle.load(open(path))

    def predict(self, instances):
        return self.pipeline.predict(instances)

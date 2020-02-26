import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from string import punctuation
from sklearn.naive_bayes import MultinomialNB
from tweet_classifier import TweetClassifier
from twokenize import tokenizeRawTweetText
from customstopword import getstopwords  

stopwords = getstopwords ()
def text_preprocessor(text):
    text = text.rstrip()
    # remove punctuation
    text = ''.join([char for char in text if char not in punctuation])
    words = [w.strip() for w in text.split()]
    return ' '.join(words)

if __name__ == '__main__':
    
    #screen_names = input("Enter the list of twitter accounts, seperate by comma: ")
    #screen_names = screen_names.split(',')
    #test = input("Enter a tweet to classify: ")
    pipeline = Pipeline([
                            ('vectorizer',  CountVectorizer(
                                                preprocessor=text_preprocessor,
                                                stop_words=stopwords,
                                                tokenizer=tokenizeRawTweetText,
                                                ngram_range=(2, 4),
                                                max_features=200,
                                                min_df=1,
                                                )),
                            ('tfidf', TfidfTransformer(use_idf=True, norm='l2')), #l2: norm 2, meaning: refer to https://scikit-learn.org
                            ('classifier',  MultinomialNB())
                        ])

    #test = ['inserts ham sandwich'] 'health care' 'protect voting rights'
    test = ['climate change']
    print('Tweet :%s' % test)
    
    screen_names = ['BarackObama','realdonaldtrump']
    classifier = TweetClassifier(screen_names, pipeline=pipeline)
    classifier.cross_validate(n_folds=5, pos_label=screen_names[0])
    classifier.train()


    print (classifier.predict(test))

    print ('Saving Model.....')
    filename = classifier.save_model('models')

    print ('Loading model and trying again....')
    model = pickle.load(open('models/'+filename,'rb'))

    print (model.predict(test))

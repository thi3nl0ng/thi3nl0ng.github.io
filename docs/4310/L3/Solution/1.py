import random

import nltk
from nltk.corpus import movie_reviews, wordnet
from nltk.classify import apply_features

# get all movie reviews(wordlist, category)
movieReviews = [
    (list(movie_reviews.words(fileid)), category)
    for category in movie_reviews.categories()
    for fileid in movie_reviews.fileids(category)
]

# randomize the documents
random.shuffle(movieReviews)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())

# Get the top synsets 2000 words
word_features = list(all_words.keys())[:2000]

def lexicon_features(reviews):
    review_words = set(reviews)
    features = dict()

    for word in word_features:
        features['contains({})'.format(word)] = (word in review_words)
        for synset in wordnet.synsets(word):
            for name in synset.lemma_names():
                features['synset({})'.format(name)] = (name in review_words)

    return features

def Lab3_E1():
    print ('Lab3, Exercise 1')
    train_set, test_set = apply_features(lexicon_features, movieReviews[100:]), apply_features(lexicon_features, movieReviews[:100])
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print (nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(10)
    
if __name__ == '__main__':
    input("\nPress ENTER for task")       
    Lab3_E1()


import tweepy
import csv
import json
import nltk
from nltk.corpus import stopwords
import re
# credentials
consumer_key = ''
consumer_secret = ''
access_key  = ''
access_secret  = ''

def get_all_tweets(screen_name):

    # Authorization and initialization

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialization of a list to hold all Tcompressionweets

    all_the_tweets = []
    res = False
    # We will get the tweets with multiple requests of 200 tweets each
    while(res == False):
        try:
            new_tweets = api.user_timeline(screen_name=screen_name, count=200,tweet_mode='extended', include_rts=True, compression=False)
            res = True
        except tweepy.TweepError as e:
            screen_name = input("The account you entered was invalid, please try again: ")
            continue
   
    # saving the most recent tweets

    all_the_tweets.extend(new_tweets)

    # save id of 1 less than the oldest tweet

    oldest_tweet = all_the_tweets[-1].id - 1
    #print(oldest_tweet)
    # grabbing tweets till none are left

    while len(new_tweets) > 0:
        # The max_id param will be used subsequently to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name,
                count=200, max_id=oldest_tweet,tweet_mode='extended', include_rts=True, compression=False)

        # save most recent tweets

        all_the_tweets.extend(new_tweets)

        # id is updated to oldest tweet - 1 to keep track

        oldest_tweet = all_the_tweets[-1].id - 1
        print ('downloaded %s tweets' % len(all_the_tweets))
    outtweets = []
    for tw in all_the_tweets:
        if hasattr(tw, "retweeted_status"):
            outtweets.append([tw.id_str, tw.created_at,
                 tw.retweeted_status.full_text])
        else:
            outtweets.append([tw.id_str, tw.created_at,
                 tw.full_text])           
    

    # writing to the csv file
    with open(screen_name + '_tweets.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(outtweets)
        
def loadcorpus(path, account):
	my_corpus = nltk.corpus.PlaintextCorpusReader(path,'.*')	
	
	if (account == "*"):
		tweets = my_corpus.raw()
	else:
		tweets = my_corpus.raw(account)
	return 	tweets
	#word_tokens = TweetTokenization(tweets)
	#return word_tokens
	#hash_tags = extract_hash_tags(tweets)	
	#fdist = nltk.FreqDist([w for w in word_tokens if w.isalpha() and len(w) >1 and not w.lower() in stop_words] )
	#return fdist


def tweet_tokenization(tweets):
    regex_str = [    
		r'<[^>]+>', # HTML tags
		r'(?:@[\w_]+)', # @-mentions
		r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
		r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
                r'&amp;', # &amp; tags
		r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
		r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
		r'(?:[\w_]+)', # other words
		r'(?:\S)' # anything else
            ]
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

    stop_words = set(stopwords.words('english'))
    word_tokens = tokens_re.findall(tweets)
    
    return [w for w in word_tokens if w.isalpha() and len(w) >1 and not w.lower() in stop_words]

def extract_hash_tags(s):
	return [('#'+ k) for k in re.findall(r"#(\w+)", s)]

if __name__ == '__main__':

    #1. Get tweets of a user
    get_all_tweets(input("Enter the twitter account: "))
	
    #2. Do load corpus and some statistics
  
    screen = input("Enter the twitter account: ")
    if (screen != "*"):
        screen = screen + '_tweets.csv'

    tweets_text = loadcorpus(r"D:\Norway\Teaching Assistant\2020 Spring\Labs\Lab1\Solution\datasets",screen)
    word_tokens = tweet_tokenization(tweets_text)
    num = int(input("Enter the number of common words: "))
    
    fdist = nltk.FreqDist( word_tokens )
    wl = fdist.most_common()[0:num]
    for w in wl:
        print ('The most common word is "%s" with frequency %s' % (w[0], w[1]))

    #2b. hashtags
    hash_tags = extract_hash_tags(tweets_text)    
    fdist = nltk.FreqDist( hash_tags )
    num = int(input("Enter the number of the most common hash_tags: "))
    wl = fdist.most_common()[0:num]
    for w in wl:
        print ('The most common hash_tags is "%s" with frequency %s' % (w[0], w[1]))

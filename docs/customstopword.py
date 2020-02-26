from nltk.corpus import stopwords 
def getstopwords():
	stopwords_1 = set(stopwords.words('english'))
	stopwords_2 = set([word.rstrip() for word in open('stopwords.txt', 'r')])
	stopwords_english = list(set(stopwords_1 | stopwords_2))
	return stopwords_english
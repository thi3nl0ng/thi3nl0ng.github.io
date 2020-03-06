import nltk
from nltk.corpus import brown
from nltk.corpus import nps_chat

def getMostFrequency(corpus):
    tagged = corpus.tagged_words()
    tag_fd = nltk.FreqDist(tag for (word, tag) in tagged)
    return tag_fd.max()


def DefaultTagger(corpus, percent, df, option = 1 ):
    if (option == 1):
        tagged_sents = corpus.tagged_sents()
    else:
        tagged_sents = corpus.tagged_posts()
    size = int(len(tagged_sents) * percent)
    train_sents = tagged_sents[:size]
    test_sents = tagged_sents[size:]    
    tagger = nltk.DefaultTagger(df)    
    print("Accuracy is ", tagger.evaluate(test_sents))
    
def CombiningTagger(corpus, percent, df, option = 1):    
    if (option == 1):
        tagged_sents = corpus.tagged_sents()
    else:
        tagged_sents = corpus.tagged_posts()
    size = int(len(tagged_sents) * percent)
    train_sents = tagged_sents[:size]
    test_sents = tagged_sents[size:]

    patterns = [
	(r'.*ing$', 'VBG'),               # gerunds
	(r'.*ed$', 'VBD'),                # simple past
	(r'.*es$', 'VBZ'),                # 3rd singular present
	(r'.*ould$', 'MD'),               # modals
	(r'.*\'s$', 'NN$'),               # possessive nouns
	(r'(The|the|A|a|An|an)$','AT'),   # determiner
	(r'.*(able|ful|ious|ble|ic|ive|est)$','JJ'),	#adjective
	(r'^a$', 'PREP'),                 # preposition
	(r'.*ly$','RB'),                  # adverb
	(r'.*s$', 'NNS'),                 # plural nouns
	(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
	(r'.*', df)                       # nouns (default)
	]

    default = nltk.DefaultTagger(df)
    tr = nltk.RegexpTagger(patterns, backoff=default)
    tu = nltk.UnigramTagger(train_sents, backoff=tr)
    tb = nltk.BigramTagger(train_sents, backoff=tu)
    print("Accuracy is ", tb.evaluate(test_sents))
if __name__ == '__main__':
    '''input("\nPress ENTER for task a")
    df = getMostFrequency(brown)
    DefaultTagger(brown, 0.5, df)
    DefaultTagger(brown, 0.9, df)
    
    df = getMostFrequency(nps_chat)
    DefaultTagger(nps_chat, 0.5, df, 0 )
    DefaultTagger(nps_chat, 0.9, df, 0)'''

    input("\nPress ENTER for task b, Combining Tagger")
    df = getMostFrequency(brown)
    CombiningTagger(brown, 0.5, df)
    CombiningTagger(brown, 0.9, df)
    
    df = getMostFrequency(nps_chat)
    CombiningTagger(nps_chat, 0.5, df, 0)
    CombiningTagger(nps_chat, 0.9, df, 0)
    

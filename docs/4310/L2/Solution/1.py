import nltk
from nltk.corpus import brown
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk.corpus import stopwords
brown_tagged = brown.tagged_words()

stop_words = set(stopwords.words('english'))
#print(brown_tagged['the'])
#1a
def TaskA():
	tags = [tag for (word, tag) in brown_tagged] #tagset='universal'
	tagDist = FreqDist(tags)
	print('The most frequent tag: ', tagDist.max(), tagDist[tagDist.max()])
	
#1b
def TaskB():
        data = nltk.ConditionalFreqDist((word.lower(), tag)
                                                for (word, tag) in brown_tagged)
        ambiguous =[(word,data[word]) for word in data.conditions() if len(data[word]) > 1 and word.lower() not in stop_words and word.isalpha()]

        print('Number of words are ambiguous: ', len(ambiguous))
        return ambiguous

#1c
def TaskC(ambiguous):
        brown_words = set(brown.words())
        percen_ambiguous = 100* len(ambiguous) / len(brown_words)
        print('The percentage of ambiguous words: ', percen_ambiguous)
#1d
def TaskD(ambiguous):
        #1d sorted(key=lambda tup:(-tup[1], tup[0]))
        
        ambiguous.sort(key=lambda x: -len(x[1]))       
        print("10 words with the greatest tags: ")
        for item in ambiguous[0:10]:
                print(item[0],' '.join(str(e) for e in item[1]) )

#1e
def TaskE(ambiguous):
        mostword = ambiguous[0][0]
        no = 0
        set_tags = [tag for tag in ambiguous[0][1]]
        tagged_sents = brown.tagged_sents()
        print("Sentences contain '", mostword, "'")
        for sent in tagged_sents:
            for (word, tag) in sent:
                for item_tag in set_tags:
                    if item_tag == tag and (word.lower() == mostword):
                        no+=1
                        print(no, sent)
                        set_tags.remove(item_tag)
                        print(5*"-----------------------")
                        break
				
if __name__ == '__main__':
        input("\nPress ENTER for task a")       
        TaskA()
        input("\nPress ENTER for task b")
        ret = TaskB()
        input("\nPress ENTER for task c")
        TaskC(ret)
        #ret = [(w[0],w[1]) for w in ret if not w[0].lower() in stopwords]
        
        input("\nPress ENTER for task d")
        TaskD(ret)
        input("\nPress ENTER for task e")
        TaskE(ret)

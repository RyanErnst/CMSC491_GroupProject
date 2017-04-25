import requests 
import html5lib
import nltk
import codecs
import russell as ru
from bs4 import BeautifulSoup

theskips = ["and",".", "to", ",", "the", "for", "in", "of", "that", "a", "on", "is", "get", "you", "has", "as", "at", "are"
,"'", "an", "with", "will", "not", "have", "would", "so","", "but",":", "be", "like", "if", "should", "also", "there", "or", "by", "per", " ",'', "As", "do"
, "he", "their", "The", "They", "he", "It", "than", "'s", "this", "''", "``", "...", "More", "our", "I", "was", "n't", "We", "any", "other"]

def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char) < 128):
			asciiText = asciiText + char
	return asciiText
#with open('Discussion.txt', 'r') as myfile:
#with open('WebpageSummary.txt', 'r') as myfile:
#	data=myfile.read().replace('\n', '')
URL = "https://www.cnet.com/products/nintendo-switch/review/"
fileObj = codecs.open("Grams.rtf","w","UTF")
html = requests.get(URL)
soup = BeautifulSoup(html.text, 'html5lib')
all_paras = soup.find_all('p')
data_2017 = ""
for para in all_paras:
	data_2017 = data_2017 + para.text

TheData = removeUnicode(data_2017)

bigWords = nltk.tokenize.word_tokenize(TheData)
N = 20
search =  nltk.BigramCollocationFinder.from_words(bigWords)
search.apply_freq_filter(2)
search.apply_word_filter(lambda skips: skips in theskips)
from nltk import BigramAssocMeasures
idxJaccard = BigramAssocMeasures.jaccard
bigrams = search.nbest(idxJaccard, N)

for bigram in bigrams:
	print str(bigram[0]).encode('utf-8'), " ", str(bigram[1]).encode('utf-8')
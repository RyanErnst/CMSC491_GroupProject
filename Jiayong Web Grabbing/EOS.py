import requests 
import html5lib
import json
import nltk
import codecs
import russell as ru
from bs4 import BeautifulSoup

theskips = ["and",".", "to", ",", "the", "for", "in", "of", "that", "a", "on", "is", "get", "you", "has", "as", "at", "are"
,"'", "an", "with", "will", "not", "have", "would", "so","", "but",":", "be", "like", "if", "should", "also", "there", "or", "by", "per", " ",'', "As", "do"
, "he", "their", "The", "They", "he", "It", "than", "'s", "this", "''", "``", "...", "More", "our", "I", "was", "n't", "We", "any", "other", "--", "'ll", "when", "more", "it", ")", "(",
"can", "its", "one", "up", "we", "i", "use", "?", "from", "my", "which", "they", "$" ,"lot", "then", "youre", "your", "about", "said"]

def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char) < 128):
			asciiText = asciiText + char
	return asciiText


URL_list = ["http://www.pcmag.com/review/348908/nintendo-switch", "https://www.cnet.com/products/nintendo-switch/review/", 
"http://www.trustedreviews.com/nintendo-switch-review", "https://www.slashgear.com/nintendo-switch-the-good-the-bad-and-the-ugly-16472025/", "http://www.techradar.com/reviews/nintendo-switch", "http://tech.firstpost.com/gaming/nintendo-switch-heres-all-you-need-to-know-about-nintendos-latest-console-357435.html",
"https://www.nytimes.com/2017/03/03/technology/review-nintendo-switch.html"]




for URL in URL_list:
	print "================================================="
	print "Eos and Frequency Distribution of ", URL
	html = requests.get(URL)
	soup = BeautifulSoup(html.text, 'html5lib')
	all_paras = soup.find_all('p')
	data_2017 = ""
	for para in all_paras:
		data_2017 = data_2017 + para.text
	TheData = removeUnicode(data_2017)
	lstSent = nltk.tokenize.sent_tokenize(TheData)

	words=[]
	for sentence in lstSent:
		for word in nltk.tokenize.word_tokenize(sentence):
			words.append(word.lower())

	frqDist = nltk.FreqDist(words)

	word_cnt = 0 
	for item in frqDist.items():
		word_cnt  = word_cnt + item[1]
	unique_word_cnt = len(frqDist.keys())
	hapaxNo = len(frqDist.hapaxes())

	mostFreq =[]
	for w in frqDist.items():
		if w[0] not in theskips:
			mostFreq.append(w)

	print "Findings"
	print 'Num lstSent:'.ljust(25), len(lstSent)
	print 'Num Words:'.ljust(25), word_cnt
	print 'Num Unique Words:'.ljust(25), unique_word_cnt
	print 'Num Hapaxes:'.ljust(25), hapaxNo
	print "The most frequent words follow "

	mostFreq.sort(key=lambda c:c[1])
	for w in mostFreq[-10:]:
		print w[0].encode('utf-8'), " \thas a count of ", w[1]




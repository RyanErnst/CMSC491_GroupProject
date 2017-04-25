import requests 
import html5lib
import russell as ru
from bs4 import BeautifulSoup

def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char) < 128):
			asciiText = asciiText + char
	return asciiText


for i in range(27, 38):	

	URL  = "https://www.trekbbs.com/threads/nintendo-nx-switch-discussion.284498/page-"
	URL += str(i)
	print(URL)
	SummaryFile  = open("Discussion.txt", "a")
	webpage = requests.get(URL)
	html = webpage.text
	soup = BeautifulSoup(html, 'html5lib')
	all_paras = soup.find_all('blockquote')
	data_2017 = ""
	for para in all_paras:
		data_2017 = data_2017 + para.text

	summary = ru.summarize(data_2017)
	print "Print Three Sentence Summary"
	for sent in summary['top_n_summary']:
		SummaryFile.write(removeUnicode(sent))
		SummaryFile.write("\n")

	SummaryFile.write("=============================")
	SummaryFile.close()
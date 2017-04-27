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

URL_list = ["http://www.pcmag.com/review/348908/nintendo-switch", "https://www.cnet.com/products/nintendo-switch/review/", 
"http://www.trustedreviews.com/nintendo-switch-review", "https://www.slashgear.com/nintendo-switch-the-good-the-bad-and-the-ugly-16472025/", "http://www.techradar.com/reviews/nintendo-switch", "http://tech.firstpost.com/gaming/nintendo-switch-heres-all-you-need-to-know-about-nintendos-latest-console-357435.html",
"https://www.nytimes.com/2017/03/03/technology/review-nintendo-switch.html"]

open("Discussion.txt", 'w').close()
open("WebpageSummary.txt", 'w').close()

print " The Summary of Nintendo Discussion Website"
for i in range(27, 38):	

	URLD  = "https://www.trekbbs.com/threads/nintendo-nx-switch-discussion.284498/page-"
	URLD += str(i)
	print(URLD)
	SummaryFile1  = open("Discussion.txt", "a")
	webpage1 = requests.get(URLD)
	html1 = webpage1.text
	soup1 = BeautifulSoup(html1, 'html5lib')
	all_paras1 = soup1.find_all("blockquote", { "class" : "messageText SelectQuoteContainer ugc baseHtml" })
	data_20171 = ""
	for para in all_paras1:
		data_20171 = data_20171 + para.text

	summary1 = ru.summarize(data_20171)
	print "Print Three Sentence Summary of page ", i 
	for sent in summary1['top_n_summary']:
		print removeUnicode(sent).strip()
		SummaryFile1.write(removeUnicode(sent).strip())
		SummaryFile1.write("\n")
    
	print ("============================")
	SummaryFile1.write("=============================")
	SummaryFile1.close()

print " The Summary of Nintendo Rating Website"
for URL in URL_list:
	SummaryFile  = open("WebpageSummary.txt", "a")
	webpage = requests.get(URL)
	html = webpage.text
	soup = BeautifulSoup(html, 'html5lib')
	all_paras = soup.find_all('p')
	data_2017 = ""
	for para in all_paras:
		data_2017 = data_2017 + para.text

	summary = ru.summarize(data_2017)
	print "Print Three Sentence Summary of Rating website ", URL
	for sent in summary['top_n_summary']:
		print removeUnicode(sent).strip()
		SummaryFile.write(removeUnicode(sent).strip())
		SummaryFile.write("\n")
	print ("============================")
	SummaryFile.write("=============================")
	SummaryFile.close()













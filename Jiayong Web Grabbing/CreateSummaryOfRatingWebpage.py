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


URL_list = ["http://www.pcmag.com/review/348908/nintendo-switch", "https://www.cnet.com/products/nintendo-switch/review/", "http://www.ign.com/articles/2017/03/08/nintendo-switch-review",
"http://www.trustedreviews.com/nintendo-switch-review", "https://www.slashgear.com/nintendo-switch-the-good-the-bad-and-the-ugly-16472025/", "http://www.techradar.com/reviews/nintendo-switch", "http://tech.firstpost.com/gaming/nintendo-switch-heres-all-you-need-to-know-about-nintendos-latest-console-357435.html",
"https://www.nytimes.com/2017/03/03/technology/review-nintendo-switch.html"]





for URL in URL_list:

	
#https://www.trekbbs.com/threads/nintendo-nx-switch-discussion.284498/page-27 
#URL = "https://www.reddit.com/r/truegaming/comments/58h2qz/nintendo_switch_reveal_discussion_thread/?st=j1wl9csr&sh=892c65de" 
	SummaryFile  = open("WebpageSummary.txt", "a")
	webpage = requests.get(URL)
	html = webpage.text
	soup = BeautifulSoup(html, 'html5lib')
	all_paras = soup.find_all('p')
	data_2017 = ""
	for para in all_paras:
		data_2017 = data_2017 + para.text

	summary = ru.summarize(data_2017)
	print "Print Three Sentence Summary"
	for sent in summary['top_n_summary']:
		SummaryFile.write(removeUnicode(sent))
		SummaryFile.write("\n")

	SummaryFile.close()
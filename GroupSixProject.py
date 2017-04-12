# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:28:12 2017

@author: Ryan
"""

import twitter
import json
import requests
import html5lib
from bs4 import BeautifulSoup
from collections import Counter
from prettytable import PrettyTable
from twython import TwythonStreamer
from collections import Counter
import datetime
import time
import string
import russell as ru
import codecs
import nltk
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

def removeUnicode(text):
    asciiText = ""
    for char in text:
        if(ord(char)<128):
            asciiText = asciiText + char
            
    return asciiText

#Twitter Specific Functions

CONSUMER_KEY = 'INSERT YOURS HERE'
CONSUMER_SECRET = 'INSERT YOURS HERE'
OAUTH_TOKEN = 'INSERT YOURS HERE'
OAUTH_TOKEN_SECRET = 'INSERT YOURS HERE'

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
tw = twitter.Twitter(auth=auth)

companyList = []
count = 100

#gathering Tweets
q = '@SOME TECH COMPANY'
lexicalCompany = []
companyLikes = []
companyRetweets = []
companySentiment = []
x = 0
for status in tw.search.tweets(q=q,count=count)["statuses"]:
    if status["lang"]=='en':
        if x < 25:
            x = x + 1
            test_str1 = json.dumps(status["text"]).encode('utf-8')
            vs1 = vaderSentiment(test_str1)
            cokeLike = json.dumps(status["favorite_count"])
            cokeRetweet = json.dumps(status["retweet_count"])
            
            #Tracking Tweet Messages
            companyList.append(test_str1)
            
            #Tracking Likes
            companyLikes.append(cokeLike)
            
            #Tracking Retweet Count
            companyRetweets.append(cokeRetweet)
            
            #Tracking Sentiment Analysis
            companySentiment.append(str(vs1['compound']))
            
            companyWords2 = []
            
            for w in test_str1.split():
                companyWords2.append(w)
                
            cntCompany2 = Counter(companyWords2)
            
            pt3 = PrettyTable(field_names=['Word','Count'])
            srtCnt3 = sorted(cntCompany2.items(),key=lambda pair: pair[1],reverse=True)
            for kv in srtCnt3:
                pt3.add_row(kv)
            
            #Tracking Lexical Diversity
            lexicalCompany.append(1.0*len(set(companyWords2))/len(companyWords2))
x = 0

#Outputing to a file for dendogram in R
file = open("companyTweets.csv","w")
for text in companyList:
    file.write(text)
    file.write("\n")
file.close()

#Outputing a "PrettyTable" for Frequency Analysis
companyWords = []
for text in companyList:
    for w in text.split():
        companyWords.append(w)

cntCompany = Counter(companyWords)

pt1 = PrettyTable(field_names=['Word','Count'])
srtCnt1 = sorted(cntCompany.items(),key=lambda pair: pair[1],reverse=True)
for kv in srtCnt1:
    pt1.add_row(kv)

lexCompany = 1.0*len(set(companyWords))/len(companyWords)

file2 = open("PythonOutput.txt", "w")
print "!=====================COKE===========================!"
file2.write("!=====================COKE===========================!\n")
y = 1
for x in range(0,25):
   print "%s: %s" %(y, companyList[x])
   file2.write("%s: %s\n" %(y, companyList[x]))
   print "Lexical Diversity: %s" %(lexicalCompany[x])
   file2.write("Lexical Diversity: %s\n" %(lexicalCompany[x]))
   print "Likes: %s" %(companyLikes[x])
   file2.write("Likes: %s\n" %(companyLikes[x]))
   print "Retweets: %s" %(companyRetweets[x])
   file2.write("Retweets: %s\n" %(companyRetweets[x]))
   print "Sentiment Analysis: %s\n" %(companySentiment[x])
   file2.write("Sentiment Analysis: %s\n\n" %(companySentiment[x]))
   y = y + 1

print "====================================="
file2.write("=====================================\n")
print "Total Lexical Diversity"
file2.write("Total Lexical Diversity\n")
print lexCompany
file2.write("%s\n\n" %(lexCompany))

print "====================================="
file2.write("=====================================\n")
print "Frequency Analysis"
file2.write("Frequency Analysis\n")
print pt1
file2.write("%s\n" %(pt1))
print "\n"
file2.write("\n")

#Screen Scraping Specific Functions
fileObj = codecs.open("GroupSixProject.rtf", "w", "UTF")
html = requests.get("COMPANY WEBPAGE(S)")

soup = BeautifulSoup(html.text,'html5lib')
all_paras = soup.find_all('p')

#MORE TO BE DETERMINED/ENTERED
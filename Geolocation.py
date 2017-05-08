# CMSC 491 Group Project - Geolocation of Nintendo Tweets
# Richard Buck - rbuck2@umbc.edu

import matplotlib.pyplot as ply
import matplotlib.patches as mpathces
from matplotlib.collections import PathCollection
from string import ascii_uppercase
import re
import matplotlib.cm as cm
import numpy as np
import numpy.random as npr
import os
import csv
from collections import Counter
from operator import itemgetter
from prettytable import PrettyTable
import json
from geopy import geocoders
from geopy.exc import GeocoderTimedOut
import twitter


def getState(myGeoCode):
    pattern = re.compile('.*([A-Z]{2}).*') 
    result = pattern.search(myGeoCode[0])
    if result == None:
        print "not found: ", myGeoCode
        return "nAck"
    elif len(result.groups()) == 1:
        return result.groups()[0]
    else:
        print "not found: ", result.groups()
        return "nAck"

def removeUnicode(text):
    asciiText=""
    for char in text:
        if(ord(char) < 128):
            asciiText = asciiText + char

    return asciiText

Bing_Key = 'Insert Bing Key Here'
g = geocoders.Bing(Bing_Key)


#tweet stuff here
CONSUMER_KEY = 'INSERT YOURS HERE'
CONSUMER_SECRET = 'INSERT YOURS HERE'
OAUTH_TOKEN = 'INSERT YOURS HERE'
OAUTH_TOKEN_SECRET = 'INSERT YOURS HERE'

auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
tw = twitter.Twitter(auth=auth)

# search parameters
q = 'nintendo switch'
count = 100

tweetCoords = []

# gather tweets
for status in tw.search.tweets(q=q,count=count)["statuses"]:

    # get coordinate object
    coords = status["coordinates"]
    print coords
       
    if coords is not None:

        # twitter originally stores coordinates as [long, lat]
        lat = str(coords["coordinates"][1])         
        lon = str(coords["coordinates"][0])
  
        # store instead as [lat, long] in string for geocoder
        tweetCoords.append(lat + ", " + lon)
    

resultList = []

# match coordinates to locations
for coord in tweetCoords:
    gmr = g.reverse(coord, exactly_one=True, timeout=4.1)
    
    if gmr == []: continue
    
    extracted_St = getState(gmr)

    if extracted_St != "nAck":
        resultList.append(extracted_St)

# print a pretty table of tweet locations
pt = PrettyTable(field_names=['State','Count'])
c = Counter(resultList)
[pt.add_row(kv) for kv in c.most_common(52)]
pt.align['State'], pt.align['count'] = 'l','r'
print pt
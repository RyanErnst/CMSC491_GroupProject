# CMSC 491 Group Project - Geolocation of Nintendo Tweets
# Richard Buck - rbuck2@umbc.edu

from string import ascii_uppercase
from collections import Counter
from prettytable import PrettyTable
import json
from geopy import geocoders
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

Bing_Key = 'gCXwcfiiO8seIP8ABtyA~FXYzdasnrBzLGd5Fz5McYg~Ar3fRJl1fYTp7XmS9cZJ09cpBYu73oTePDCLnYE9eMtDNXB0X3GDjK7-hg92xuTq'
g = geocoders.Bing(Bing_Key)


#tweet stuff here
CONSUMER_KEY = 'jntLw4dJ8p22qqzLZ8TTMiK1c'
CONSUMER_SECRET = 'HqjcJ2XOuaHikVLc6Qnj6jUvnNc1ItYTbz8ZHmu7N1M4m5xEjW'
OAUTH_TOKEN = '82240277-ZhAxe3ZOHEFr9faEpEaq1jcfVqrCmiK0aH9LXAa17'
OAUTH_TOKEN_SECRET = 'xyUinyofNgpK4zaLRebBTdIMTwLf4pclvLFs01WeYnPda'

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
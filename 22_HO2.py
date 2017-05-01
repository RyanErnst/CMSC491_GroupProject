import facebook
import json
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import nltk

def removeUnicode(text):
    asciiText=""
    for char in text:
        if(ord(char) < 128):
            asciiText = asciiText + char

    return asciiText

ACCESS_TOKEN = 'New Token'

fb = facebook.GraphAPI(ACCESS_TOKEN)

#Query for the Right Nintendo switch page, uncomment JSON dumps to see IDs
djt = fb.request('search', {'q':'Nintendo Switch', 'type': 'page', 'limit':5})
#print json.dumps(djt, indent=1)

#Switch ID
switch = '1125429570886433'

#Dict of Posts
d_posts = fb.get_connections(switch, 'posts')

#Total Switch Page Likes
print "\nTotal Nintendo Switch Likes: %d" % (fb.get_object(switch)['likes'])+"\n"

vs_tot = 0
vs_pot = 0
vs_neg = 0
num_cmt = 0

#Loop Through details of 10 Posts
for i in range(0,10):
    print "##### Post Number :" + str(i+1) + " #####\n"

    #All posts dont necessarily have a message, i.e. a shared video with no message
    if 'message' in d_posts['data'][i]:
        print removeUnicode(d_posts['data'][i]['message']) #Ones with a message

    else:
        print removeUnicode(d_posts['data'][i]['story']) #Without a message i.e. "Nintendo shared a Video.."

    print
    print "Total Post Likes: "
    test = fb.get_connections(d_posts['data'][i]['id'], 'likes?summary=1')
    print test['summary']['total_count'] #Total likes on the post
    print
    
    print "##### Comment 1 #####\n"
    print removeUnicode(d_posts['data'][1]['comments']['data'][i]['message']) #Message from first comment
    print
    print "Commenter Name: " + d_posts['data'][1]['comments']['data'][i]['from']['name'] #Name
    print "Comment Like Count: " + str(d_posts['data'][1]['comments']['data'][i] ['like_count']) #Like Count
    print
	
	# Sentiment analysis per comment
	vs = vaderSentiment(dataItem['message'].encode('utf-8'))
	print "Sentiment: " + str(vs['compound'])
	vs_tot = vs_tot + vs['compound']
	num_cmt = num_cmt + 1
	if vs['compound'] < 0:
		vs_neg = vs_neg + 1
	else:
		vs_pos = vs_pos + 1

# Sentiment analysis overall
print "Overall sentiment is %f, pos %d, neg %d" % ((vs_tot / num_cmt)), vs_pos, vs_neg)

#Frequency distribution
frqDist = nltk.FreqDist(words)

word_cnt = 0
for item in frqDist.items():
	word_cnt = word_cnt + item[1]
unique_word_cnt = len(frqDist.keys())

print("Lexical diversity is %f" % (1.0 * unique_word_cnt / word_cnt)

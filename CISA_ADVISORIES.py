#from langchain.tools import tool
import feedparser
CISA_Feed = 'https://www.cisa.gov/cybersecurity-advisories/all.xml'

#@tool
def cisa_get_feed():
    feed = feedparser.parse(CISA_Feed)
    count = 0
    feedDescriptions = []
    #feedTitles = []
    for entry in feed.entries:
        count += 1
        if count >= 5:
            break
        else:
            feedDescriptions.append(entry.description)
            #feedTitles.append(entry.title)
    #s = '\n'
    #s.join(feedDescriptions)
    return feedDescriptions

def cisa_get_titles():
    feed = feedparser.parse(CISA_Feed)
    count = 0
    feedTitles = []
    for entry in feed.entries:
        count += 1
        if count >= 5:
            break
        else:
            feedTitles.append(entry.title)
    return feedTitles


#print(cisa_get_feed())

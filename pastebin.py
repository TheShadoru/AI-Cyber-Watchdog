from duckduckgo_search import DDGS
import json
import requests
import datetime
from ollama import Client
client = Client(host='http://127.0.0.1:11434')

llm_model = 'llama3'

def SearchPastebin(searchTerms):
    print("\nSearching pastebin for: {0}...".format(searchTerms))
    results = DDGS().text((searchTerms + ' site:pastebin.com'), safesearch='off')
    fdtn = str((datetime.datetime.now().day)) + str((datetime.datetime.now().month)) + str((datetime.datetime.now().year)) + str((datetime.datetime.now().hour)) + str((datetime.datetime.now().minute)) + str((datetime.datetime.now().second))
    file = open("pastebin_report_{0}.txt".format(fdtn), "a")
    file.write("\nSearch for: {0}".format(searchTerms))
    file.write("\n\n\n")
    for item in results:
        print("\n")
        fullReport = ''
        link = (str(item).split("href': '")[1].split("', ")[0]).split("pastebin.com/")[1]
        file.write(link + " ::\n")
        #print(link)
        link = "https://pastebin.com/raw/" + link
        res = requests.get(link)
        file.write(res.text + "\n\n")
        print(link)
        print("\n")
        stream = client.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': '{0}. Provide a summary of this text. If there is any content that references vulnerabilities, exploits, or hacking, the please highlight that.'.format(res.text)}],
            stream=True,
        )
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            fullReport = fullReport + chunk['message']['content']
        file.write("\n{0}".format(fullReport))
    file.close()
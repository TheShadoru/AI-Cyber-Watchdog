from duckduckgo_search import DDGS
import json
import requests
import datetime
from ollama import Client

def SearchPastebin(searchTerms, configuration, fdtn):
    
    if len(configuration.globalConfig['PASTEBIN']['OLLAMA_URL']) > 0:
        client = Client(host=configuration.globalConfig['PASTEBIN']['OLLAMA_URL'])
    else:
        client = Client(host=configuration.globalConfig['GLOBAL']['OLLAMA_URL'])

    if len(configuration.globalConfig['PASTEBIN']['LLM']) > 0:
        llm_model = configuration.globalConfig['PASTEBIN']['LLM']
    else:
        llm_model = configuration.globalConfig['GLOBAL']['LLM']
    
    
    print("\nSearching pastebin for: {0}...".format(searchTerms))
    
    results = DDGS().text((searchTerms + ' site:pastebin.com'), safesearch='off')
    
    file = open("./reports/pastebin_report_{0}.txt".format(fdtn), "a")
    file.write("\nSearch for: {0}\n\n\n".format(searchTerms))
    
    for item in results:
        fullReport = ''
        link = (str(item).split("href': '")[1].split("', ")[0]).split("pastebin.com/")[1]
        file.write(link + " ::\n")
        #print(link)
        link = "https://pastebin.com/raw/" + link
        res = requests.get(link)
        file.write(res.text + "\n\n")
        print("\n{0}\n".format(link))
        
        stream = client.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': '{0} {1}'.format(res.text, configuration['PASTEBIN']['PROMPT'])}],
            stream=True,
        )
        
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            fullReport = fullReport + chunk['message']['content']
        file.write("\n{0}".format(fullReport))
    file.close()
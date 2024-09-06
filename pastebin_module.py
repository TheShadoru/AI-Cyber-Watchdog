from duckduckgo_search import DDGS
import json
import requests
import datetime
from ollama import Client
from groq import Groq
import inference_module
import sql_module

def SearchPastebin(searchTerms, configuration, fdtn):
    
    if configuration.globalConfig['GLOBAL']['USE_OLLAMA']:
        if len(configuration.globalConfig['PASTEBIN']['OLLAMA_LLM']) > 0:
            llm_model = configuration.globalConfig['PASTEBIN']['OLLAMA_LLM']
        else:
            llm_model = configuration.globalConfig['GLOBAL']['OLLAMA_LLM']
        if len(configuration.globalConfig['PASTEBIN']['OLLAMA_URL']) > 0:
            client = Client(host=configuration.globalConfig['PASTEBIN']['OLLAMA_URL'])
        else:
            client = Client(host=configuration.globalConfig['GLOBAL']['OLLAMA_URL'])
    else:
        if len(configuration.globalConfig['PASTEBIN']['GROQ_LLM']) > 0:
            llm_model = configuration.globalConfig['PASTEBIN']['GROQ_LLM']
        else:
            llm_model = configuration.globalConfig['GLOBAL']['GROQ_LLM']
        usingOllama = False
    
    
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
        print("\nSource: {0}\n".format(link))
        if usingOllama:
            aiReport = inference_module.ollamaInference(res.text, configuration.globalConfig['PASTEBIN']['PROMPT'], client, llm_model)
            fullReport = fullReport + aiReport
        else:
            aiReport = inference_module.groqInference(res.text, configuration.globalConfig['PASTEBIN']['PROMPT'], configuration, llm_model)
            fullReport = fullReport + aiReport
        file.write("\n{0}".format(fullReport))
    file.close()
    if configuration.globalConfig['GLOBAL']['USE_SQLITE3']:
        sql_module.writeData(fdtn, configuration.globalConfig['PASTEBIN']['PROMPT'], results, fullReport)

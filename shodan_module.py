#import ollama
import shodan_tools
from ollama import Client
from groq import Groq
import inference_module

def startShodan(searchQuery, configuration, fdtn):
    if configuration.globalConfig['GLOBAL']['USE_OLLAMA'] == True:
        if len(configuration.globalConfig['SHODAN']['OLLAMA_LLM']) > 0:
            llm_model = configuration.globalConfig['SHODAN']['OLLAMA_LLM']
        else:
            llm_model = configuration.globalConfig['GLOBAL']['OLLAMA_LLM']
        if len(configuration.globalConfig['SHODAN']['OLLAMA_URL']) > 0:
            client = Client(host=configuration.globalConfig['SHODAN']['OLLAMA_URL'])
        else:
            client = Client(host=configuration.globalConfig['GLOBAL']['OLLAMA_URL'])
    else:
        usingOllama = False
        client = Groq(api_key=configuration.globalConfig['GROQ']['API_KEY'])

    shodanReport = shodan_tools.shodan_org_scan(searchQuery, configuration.globalConfig['SHODAN']['API_KEY'])
    print('\nShodan Report:\n{0}\n\n'.format(shodanReport))


    fullReport = ''

    if len(shodanReport) > 0:
        if usingOllama:
            aiReport = inference_module.ollamaInference(shodanReport, configuration.globalConfig['SHODAN']['PROMPT'], client)
            fullReport = fullReport + aiReport
        else:
            aiReport = inference_module.groqInference(shodanReport, configuration.globalConfig['SHODAN']['PROMPT'], configuration)
            fullReport = fullReport + aiReport
        
        file = open("./reports/shodan_report_{0}.txt".format(fdtn), "a")
        file.write("\nSearch for: {0}\n[SHODAN REPORT]:\n{1}\n[AI REPORT]:\n{2}".format(searchQuery,shodanReport,fullReport))
        file.close()
    else:
        print("No information found.")
        file.write("\nSearch for: {0}\n[SHODAN REPORT]:\nNo information found.".format(searchQuery,shodanReport))

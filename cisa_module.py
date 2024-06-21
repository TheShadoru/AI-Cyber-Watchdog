#import shodan_tools
import cisa_search
from ollama import Client

def startCisa(configuration, fdtn):
    print("Analyzing CISA Avisories...")
    if len(configuration.globalConfig['CISA']['OLLAMA_URL']) > 0:
        client = Client(host=configuration.globalConfig['CISA']['OLLAMA_URL'])
    else:
        client = Client(host=configuration.globalConfig['GLOBAL']['OLLAMA_URL'])

    if len(configuration.globalConfig['CISA']['LLM']) > 0:
        llm_model = configuration.globalConfig['CISA']['LLM']
    else:
        llm_model = configuration.globalConfig['GLOBAL']['LLM']

    cisaReports = cisa_search.cisa_get_feed()
    #print(len(cisaReports))
    cisaTitles = cisa_search.cisa_get_titles()

    count = 0
    fullReport = ''
    file = open("./reports/cisa_report_{0}.txt".format(fdtn), "a")
    for item in cisaReports:
        try:
            equipment = item.split("<li><strong>Equipment</strong>: ")[1].split("</li>")[0]
            fullReport = fullReport + ("\n{0}".format(equipment))
            print("Equipment: {0}".format(equipment))
        except:
            print("No equipment")
        try:
            vendor = item.split("<li><strong>Vendor</strong>: ")[1].split("</li>")[0]
            fullReport = fullReport + ("\n{0}".format(vendor))
            print("Vendor: {0}".format(vendor))
        except:
            print("No vendor")
        
        print("\n------------------------------------------------\n{0}\n".format(cisaTitles[count]))
        count = count + 1
        stream = client.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': '{0} {1}'.format(item, configuration.globalConfig['CISA']['PROMPT'])}],
            stream=True,
        )
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            fullReport = fullReport + chunk['message']['content']
    file.write(str(cisaReports))
    file.write("\n\n\n")
    file.write(fullReport)
    file.close()
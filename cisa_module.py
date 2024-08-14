#import shodan_tools
import cisa_search
from ollama import Client
from groq import Groq
import inference_module

def startCisa(configuration, fdtn):
    usingOllama = True
    print("Analyzing CISA Advisories...\nSource: https://www.cisa.gov/cybersecurity-advisories/all.xml")
    if configuration.globalConfig['GLOBAL']['USE_OLLAMA'] == True:
        if len(configuration.globalConfig['CISA']['OLLAMA_LLM']) > 0:
            llm_model = configuration.globalConfig['CISA']['OLLAMA_LLM']
        else:
            llm_model = configuration.globalConfig['GLOBAL']['OLLAMA_LLM']
        if len(configuration.globalConfig['CISA']['OLLAMA_URL']) > 0:
            client = Client(host=configuration.globalConfig['CISA']['OLLAMA_URL'])
        else:
            client = Client(host=configuration.globalConfig['GLOBAL']['OLLAMA_URL'])
    else:
        if len(configuration.globalConfig['CISA']['GROQ_LLM']) > 0:
            llm_model = configuration.globalConfig['CISA']['GROQ_LLM']
        else:
            llm_model = configuration.globalConfig['GLOBAL']['GROQ_LLM']
        usingOllama = False


    cisaReports = cisa_search.cisa_get_feed()
    #print(len(cisaReports))
    cisaTitles = cisa_search.cisa_get_titles()

    count = 0
    fullReport = ''
    file = open("./reports/cisa_report_{0}.txt".format(fdtn), "a")
    for item in cisaReports:
        print("\n------------------------------------------------\n{0}\n".format(cisaTitles[count]))
        count = count + 1
        try:
            equipment = item.split("<li><strong>Equipment</strong>: ")[1].split("</li>")[0]
            fullReport = fullReport + ("\n{0}".format(equipment))
            print("Related Equipment found in this report: {0}".format(equipment))
        except:
            print("No related equipment (hardware/software) found in this report")
        try:
            vendor = item.split("<li><strong>Vendor</strong>: ")[1].split("</li>")[0]
            fullReport = fullReport + ("\n{0}".format(vendor))
            print("Related Vendor found in this report: {0}".format(vendor))
        except:
            print("No related vendor found in this report")
        
        if usingOllama:
            aiReport = inference_module.ollamaInference(item, configuration.globalConfig['CISA']['PROMPT'], client, llm_model)
            fullReport = fullReport + aiReport
        else:
            aiReport = inference_module.groqInference(item, configuration.globalConfig['CISA']['PROMPT'], configuration, llm_model)
            fullReport = fullReport + aiReport
    file.write(str(cisaReports))
    file.write("\n\n\n")
    file.write(fullReport)
    file.close()
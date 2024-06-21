#import ollama
import shodan_tools
from ollama import Client

def startShodan(searchQuery, configuration, fdtn):
    if len(configuration.globalConfig['SHODAN']['OLLAMA_URL']) > 0:
        client = Client(host=configuration.globalConfig['SHODAN']['OLLAMA_URL'])
    else:
        client = Client(host=configuration.globalConfig['GLOBAL']['OLLAMA_URL'])

    if len(configuration.globalConfig['SHODAN']['LLM']) > 0:
        llm_model = configuration.globalConfig['SHODAN']['LLM']
    else:
        llm_model = configuration.globalConfig['GLOBAL']['LLM']

    shodanReport = shodan_tools.shodan_org_scan(searchQuery, configuration.globalConfig['SHODAN']['API_KEY'])
    print('\nShodan Report:\n{0}\n\n'.format(shodanReport))


    AIReport = ''

    if len(shodanReport) > 0:
        stream = client.chat(
            model=llm_model,
            messages=[{'role': 'user', 'content': '{0} {1}'.format(shodanReport, configuration.globalConfig['SHODAN']['PROMPT'])}],
            stream=True,
        )

        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
            AIReport = AIReport + chunk['message']['content']
        

        file = open("./reports/shodan_report_{0}.txt".format(fdtn), "a")
        file.write("\nSearch for: {0}\n[SHODAN REPORT]:\n{1}\n[AI REPORT]:\n{2}".format(searchQuery,shodanReport,AIReport))
        file.close()
    else:
        print("No information found.")
        file.write("\nSearch for: {0}\n[SHODAN REPORT]:\nNo information found.".format(searchQuery,shodanReport))

import ollama
#import shodan_tools
import cisa_search
import datetime

llm_model = 'llama2'

cisaReports = cisa_search.cisa_get_feed()
#print(len(cisaReports))
cisaTitles = cisa_search.cisa_get_titles()

fdtn = str((datetime.datetime.now().day)) + str((datetime.datetime.now().month)) + str((datetime.datetime.now().year)) + str((datetime.datetime.now().hour)) + str((datetime.datetime.now().minute)) + str((datetime.datetime.now().second))

count = 0
fullReport = ''
for item in cisaReports:
    #print("\n---------------------------\nCISA REPORT:\n{0}\n\n".format(item))
    print("\n------------------------------------------------\n{0}\n".format(cisaTitles[count]))
    stream = ollama.chat(
        model=llm_model,
        messages=[{'role': 'user', 'content': 'Here is a report from CISA: {0}. Create a summary of only the CVEs.'.format(item)}],
        stream=True,
    )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    count = count + 1
    fullReport = fullReport + chunk['message']['content']
file = open("cisa_report_{0}.txt".format(fdtn), "a")
file.write(str(cisaReports))
file.write("\n\n\n")
file.write(fullReport)
file.close()
print("\n\nDone!")

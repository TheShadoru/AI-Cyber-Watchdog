import ollama
#import shodan_tools
import cisa_search

llm_model = 'llama2'

cisaReports = cisa_search.cisa_get_feed()
print(len(cisaReports))
cisaTitles = cisa_search.cisa_get_titles()

count = 0
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
print("\n\nDone!")

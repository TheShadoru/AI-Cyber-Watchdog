import config
import datetime
#import inference_module

def initScript():
  with open('./ASCII', 'r') as art:
    print(art.read())
  
  configuration = config.config()
  main(configuration)

def main(configuration):
  
  fdtn = str((datetime.datetime.now().day)) + str((datetime.datetime.now().month)) + str((datetime.datetime.now().year)) + str((datetime.datetime.now().hour)) + str((datetime.datetime.now().minute)) + str((datetime.datetime.now().second))

  if not configuration.globalConfig['GLOBAL']['USE_OLLAMA'] and len(configuration.globalConfig['GROQ']['API_KEY']) > 0:
    print("No Groq API key found!")
  else:
    if configuration.globalConfig['GLOBAL']['USE_SHODAN']:

      if len(configuration.globalConfig['SHODAN']['API_KEY']) > 0:

        print("\tStarting shodan module...")
        query = input("\tEnter hostname, ip(s), company name, or device to search Shodan: ")

        import shodan_module
        shodan_module.startShodan(query, configuration, fdtn)
    
      else:
        print("\tNo Shodan API key found!")

    if configuration.globalConfig['GLOBAL']['USE_CISA']:
      print("\tStarting CISA module...")
      import cisa_module
      cisa_module.startCisa(configuration, fdtn)
    
    if configuration.globalConfig['GLOBAL']['USE_PASTEBIN']:
      print("\tStarting Pastebin module...")
      import pastebin_module
      query = input("\tEnter hostname, ip(s), company name, or device to search Pastebin: ")
      pastebin_module.SearchPastebin(query, configuration, fdtn)
    
    print("\nScript complete!")


initScript()
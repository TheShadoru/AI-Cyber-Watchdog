import os
import configparser

class config:
    def __init__(self):
        config = configparser.ConfigParser()
        print("Reading config...")
        if os.path.isfile('./watchdog.ini'):
            config.read('watchdog.ini')
            self.globalConfig = {
                'GLOBAL': {
                    'USE_SHODAN': config['GLOBAL'].getboolean('USE_SHODAN'),
                    'USE_CISA': config['GLOBAL'].getboolean('USE_CISA'),
                    'USE_PASTEBIN': config['GLOBAL'].getboolean('USE_PASTEBIN'),
                    'USE_OLLAMA': config['GLOBAL']['USE_OLLAMA'],
                    'OLLAMA_URL': config['GLOBAL']['OLLAMA_URL'],
                    'OLLAMA_LLM': config['GLOBAL']['OLLAMA_LLM'],
                    'GROQ_LLM': config['GLOBAL']['GROQ_LLM']
                },
                'SHODAN': {
                    'OLLAMA_URL': config['SHODAN']['OLLAMA_URL'],
                    'API_KEY': config['SHODAN']['API_KEY'],
                    'PROMPT': config['SHODAN']['PROMPT'],
                    'OLLAMA_LLM': config['SHODAN']['OLLAMA_LLM'],
                    'GROQ_LLM': config['SHODAN']['GROQ_LLM']
                },
                'CISA': {
                    'OLLAMA_URL': config['CISA']['OLLAMA_URL'],
                    'PROMPT': config['CISA']['PROMPT'],
                    'OLLAMA_LLM': config['CISA']['OLLAMA_LLM'],
                    'GROQ_LLM': config['CISA']['GROQ_LLM']
                },
                'PASTEBIN': {
                    'OLLAMA_URL': config['PASTEBIN']['OLLAMA_URL'],
                    'PROMPT': config['PASTEBIN']['PROMPT'],
                    'OLLAMA_LLM': config['PASTEBIN']['OLLAMA_LLM'],
                    'GROQ_LLM': config['PASTEBIN']['GROQ_LLM']
                },
                'GROQ': {
                    'API_KEY': config['GROQ']['API_KEY']
                }
            }
            print("\nConfiguration loaded!")
        else:
            print("No configuration file found.\nNow creating a new configuration file called watchdog.ini in the current working directory.")
            config['GLOBAL'] = {
                '# If you wish to use Shodan, then set use_shodan to True. If not, set it to False. Find out more at: https://www.shodan.io/\n'
                'USE_SHODAN': False,
                '# If you wish to use the CISA Feed, then set use_cisa to True. If not, set it to False. Find out more at: https://www.cisa.gov/about/contact-us/subscribe-updates-cisa\n'
                'USE_CISA': True,
                '# If you wish to use Pastebin, then set use_pastebin to True. If not, set it to False\n'
                'USE_PASTEBIN': True,
                '# Do you want to use Ollama for inference? Set to True/False (Disabling Ollama Inference will enable Groq inference as the default inference source for the all modules in the AI Cyber Watchdog. You will need to provide an API key to use for Groq.)\n'
                'USE_OLLAMA': True,
                '# If you have set use_ollama = False, no further Ollama setting changes will be needed.\n'
                '# Provide a global Ollama inference url.\n'
                'OLLAMA_URL': 'http://127.0.0.1:11434',
                '# Enter a valid Ollama LLM model name as needed.\n'
                'OLLAMA_LLM': 'llama3.1',
                '# Provide a Groq LLM for the AI Cyber Watchdog to use. The default Groq model we use is: llama-3.1-8b-instant. If you wish to use a different Groq model, you must use model names as shown at https://console.groq.com/docs/models.\n'
                'GROQ_LLM': 'llama-3.1-8b-instant'
                }
            config['SHODAN'] = {
                '# provide an alternative ollama inference url if desired. (this will override the system wide ollama url setting in the “global” section above.)\n'
                'OLLAMA_URL': '<enter Ollama url here>',
                '# An API key is needed to utilize the Shodan module. You can get a Shodan API key here: https://account.shodan.io/billing\n'
                'API_KEY': '<enter Shodan API key here>',
                'PROMPT': 'Provide a summary of this report. Then, detail steps of mitigation in bullet format.',
                '# Enter a valid Ollama LLM model name as needed. (This will override the system wide Ollama LLM setting in the “global” section above.)\n'
                'OLLAMA_LLM': '<enter Ollama LLM name here>',
                '# Enter a valid Groq LLM model name as needed. (This will override the system wide Groq LLM setting in the “global” section above.)\n'
                'GROQ_LLM': '<enter Groq LLM name here>'
            }
            config['CISA'] = {
                '# provide an alternative ollama inference url if desired. (this will override the system wide ollama url setting in the “global” section above.)\n'
                'OLLAMA_URL': '<enter Ollama url here>',
                'PROMPT': 'Summarize this article from the CISA RSS Feed.',
                '# Enter a valid Ollama LLM model name as needed. (This will override the system wide Ollama LLM setting in the “global” section above.)\n'
                'OLLAMA_LLM': '<enter Ollama LLM name here>',
                '# Enter a valid Groq LLM model name as needed. (This will override the system wide Groq LLM setting in the “global” section above.)\n'
                'GROQ_LLM': '<enter Groq LLM name here>'
            }
            config['PASTEBIN'] = {
                '# provide an alternative ollama inference url if desired. (this will override the system wide ollama url setting in the “global” section above.)\n'
                'OLLAMA_URL': '<enter Ollama url here>',
                'PROMPT': 'Provide a summary of this text. If there is any content that references vulnerabilities, exploits, or hacking, the please highlight that.',
                '# Enter a valid Ollama LLM model name as needed. (This will override the system wide Ollama LLM setting in the “global” section above.)\n'
                'OLLAMA_LLM': '<enter Ollama LLM name here>',
                '# Enter a valid Groq LLM model name as needed. (This will override the system wide Groq LLM setting in the “global” section above.)\n'
                'GROQ_LLM': '<enter Groq LLM name here>'
            }
            config['GROQ'] = {
                '# An API key is needed for use with Groq inference, enter it here:\n'
                'API_KEY': '<enter Groq API key here>'
            }
            with open('watchdog.ini', 'w') as configFile:
                config.write(configFile)
            config.clear()
            print("You will now need to open the new configuration file in a text editor and update it.\nReview instructions in the configuration file and enter API keys and URLs as needed.\nIf you are on a Linux computer, type 'nano ./watchdog.ini' to open the file.\nAfter you have completed making changes, hit crtl-x to save the file and exit from Nano.\nIf you are on a Windows computer, open the configuration file called 'watchdog.ini' with Notepad. Update the file, save and close it.\nThen restart the AI Cyber Watchdog by hitting the up arrow to re-use previous command or by typing: './venv/bin/python3 main.py' at the command line and then hit enter.")
            exit()
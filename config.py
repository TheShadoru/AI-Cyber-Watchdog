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
            print("Configuration not found.\nCreating a configuration file!")
            config['GLOBAL'] = {
                'USE_SHODAN': False,
                'USE_CISA': True,
                'USE_PASTEBIN': True,
                '# Provide a global Ollama inference url.\n'
                'OLLAMA_URL': 'http://127.0.0.1:11434',
                '# Provide a global Ollama LLM to use.\n'
                'OLLAMA_LLM': 'llama3.1',
                '# Use Ollama inference? (Disabling Ollama Inference will enable Groq inference. You will need to provide an API key to use for Groq.)\n'
                'USE_OLLAMA': True,
                '# Provide a global Groq LLM to use. If a global Groq LLM is set, individual module Groq LLMs will not be used.\n'
                'GROQ_LLM': 'llama-3.1-8b-instant'
                }
            config['SHODAN'] = {
                '# Provide an Ollama inference url. (This will override the global URL.)\n'
                'OLLAMA_URL': '',
                '# An API key is needed to utilize the Shodan module.\n'
                'API_KEY': '',
                'PROMPT': 'Provide a summary of this report. Then, detail steps of mitigation in bullet format.',
                '# Provide an Ollama LLM. (This will override the global Ollama LLM.)\n'
                'OLLAMA_LLM': '',
                '# Provide a Groq LLM. (This will override the global Groq LLM.)\n'
                'GROQ_LLM': ''
            }
            config['CISA'] = {
                '# Provide an Ollama inference url. (This will override the global URL.)\n'
                'OLLAMA_URL': '',
                'PROMPT': 'Summarize this article from the CISA RSS Feed.',
                '# Provide an Ollama LLM. (This will override the global Ollama LLM.)\n'
                'OLLAMA_LLM': '',
                '# Provide a Groq LLM. (This will override the global Groq LLM.)\n'
                'GROQ_LLM': ''
            }
            config['PASTEBIN'] = {
                '# Provide an Ollama inference url. (This will override the global URL.)\n'
                'OLLAMA_URL': '',
                'PROMPT': 'Provide a summary of this text. If there is any content that references vulnerabilities, exploits, or hacking, the please highlight that.',
                '# Provide an Ollama LLM. (This will override the global Ollama LLM.)\n'
                'OLLAMA_LLM': '',
                '# Provide a Groq LLM. (This will override the global Groq LLM.)\n'
                'GROQ_LLM': ''
            }
            config['GROQ'] = {
                '# An API key is needed for use with Groq inference.\n'
                'API_KEY': ''
            }
            with open('watchdog.ini', 'w') as configFile:
                config.write(configFile)
            config.clear()
            print("Please review the new configuration and restart the program!")
            exit()
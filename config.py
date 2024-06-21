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
                    'OLLAMA_URL': config['GLOBAL']['OLLAMA_URL'],
                    'LLM': config['GLOBAL']['LLM']
                },
                'SHODAN': {
                    'OLLAMA_URL': config['SHODAN']['OLLAMA_URL'],
                    'API_KEY': config['SHODAN']['API_KEY'],
                    'PROMPT': config['SHODAN']['PROMPT'],
                    'LLM': config['SHODAN']['LLM'],
                },
                'CISA': {
                    'OLLAMA_URL': config['CISA']['OLLAMA_URL'],
                    'PROMPT': config['CISA']['PROMPT'],
                    'LLM': config['CISA']['LLM'],
                }
            }
            print("\nConfiguration loaded!")
        else:
            print("Configuration not found.\nCreating a configuration file!")
            config['GLOBAL'] = {
                'USE_SHODAN': False,
                'USE_CISA': True,
                'USE_PASTEBIN': True,
                'OLLAMA_URL': 'http://127.0.0.1:11434',
                'LLM': 'llama3'
                }
            config['SHODAN'] = {
                'OLLAMA_URL': '',
                'API_KEY': '',
                'PROMPT': 'Provide a summary of this report. Then, detail steps of mitigation in bullet format.',
                'LLM': ''
            }
            config['CISA'] = {
                'OLLAMA_URL': '',
                'PROMPT': 'Summarize this article from the CISA RSS Feed.',
                'LLM': ''
            }
            config['PASTEBIN'] = {
                'OLLAMA_URL': '',
                'PROMPT': 'Provide a summary of this text. If there is any content that references vulnerabilities, exploits, or hacking, the please highlight that.',
                'LLM': ''
            }
            with open('watchdog.ini', 'w') as configFile:
                config.write(configFile)
            config.clear()
            print("Please review the new configuration and restart the program!")
            exit()
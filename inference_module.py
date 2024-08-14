from ollama import Client
from groq import Groq

def ollamaInference(referenceData, prompt, client, inference_model):
    print("Ollama LLM model used: {0}".format(inference_model))
    AIReport = ''
    stream = ollama.Client.chat(
            model=inference_model,
            messages=[{'role': 'user', 'content': '{0} {1}'.format(prompt, referenceData)}],
            stream=True,
        )
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        AIReport = AIReport + chunk['message']['content']
    return AIReport
        
def groqInference(referenceData, prompt, configuration, inference_model):
    print("GROQ LLM model used: {0}".format(inference_model))
    client = Groq(api_key=configuration.globalConfig['GLOBAL']['GROQ_API_KEY'])
    chat_completion = client.chat.completions.create(
        messages=[{'role': 'user','content': '{0} {1}'.format(prompt, referenceData)}],
        model=configuration.globalConfig['GLOBAL']['GROQ_LLM']
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content
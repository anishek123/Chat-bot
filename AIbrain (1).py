# file path to the chat log file
chat_log_file = "C:\\Users\\KIIT\\Desktop\\adi\\mini_project\\Database\\chat_log.txt"

# file path to the API key file
api_file = "C:\\Users\\KIIT\\Desktop\\adi\\mini_project\\Data\\Api.txt"
from Body.speak import Speak
from Body.listen import MicExecution
import os

# read the API key from the file
with open(api_file, "r") as f:
    api_key = f.read().strip()

# set up the OpenAI API
import openai

openai.api_key = api_key

from dotenv import load_dotenv

load_dotenv()

from cachetools import TTLCache

model_engine = "text-davinci-002"

# Create cache for API responses
cache = TTLCache(maxsize=1000, ttl=600)

completion = openai.Completion()


def ReplyBrain(question, chat_log=None):
    # read the chat log from the file
    with open(chat_log_file, "r") as f:
        chat_log_template = f.read()

    if chat_log is None:
        chat_log = chat_log_template

    prompt = f'{chat_log}You: {question}\nMoni: '

    if prompt in cache:
        answer = cache[prompt]
    else:
        response = completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)

        answer = response.choices[0].text.strip()

        # Add response to cache
        cache[prompt] = answer

    # write the updated chat log to the file
    chat_log_template_update = chat_log_template + f"\nYou : {question} \nMoni : {answer}"
    with open(chat_log_file, "w") as f:
        f.write(chat_log_template_update)

    return answer


def open_whatsapp():
    os.startfile(
        "C:\\Users\\KIIT\\AppData\\Local\\Packages\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\\WhatsApp\\WhatsApp.exe")


while True:
    kk = MicExecution()
    kk = str(kk)
    # kk = input("Enter: ")

    if "Open Camera" in kk:
        pp = "Ok sir.. Camera is opened"
        Speak(pp)

    elif "Open WhatsApp" in kk:
        qq = "Opening WhatsApp"
        Speak(qq)
        open_whatsapp()

    else:
        reply = ReplyBrain(kk)
        Speak(reply)
        print(reply)


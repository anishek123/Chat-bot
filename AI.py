from Body.listen import MicExecution
from Brain.AIbrain import ReplyBrain
from Body.speak import Speak

print(">> Starting Mr.D: Please wait for a few seconds.")

def MainExecution():
    while True:
        # Listen for audio input from the user
        data = MicExecution()

        # If no audio input was detected, continue listening
        if data == "":
            continue

        # Generate a response based on the input
        reply = ReplyBrain(data)

        # Output the response as text-to-speech
        Speak(reply)


import os
import threading
import openai
from dotenv import load_dotenv
from cachetools import TTLCache
from Body.speak import Speak
from Body.listen import MicExecution

# Load environment variables
load_dotenv()

# Read API key and chat log file path from environment variables
API_KEY = os.getenv("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")
CHAT_LOG_FILE = os.getenv("C:\\Users\\KIIT\\Desktop\\adi\\mini_project\\Database\\chat_log.txt")

# Set up OpenAI API
openai.api_key = API_KEY
model_engine = "text-davinci-002"

# Create cache for API responses (thread-safe)
cache = TTLCache(maxsize=1000, ttl=600)
lock = threading.Lock()

# Initialize OpenAI Completion object
completion = openai.Completion(engine=model_engine)

def reply_brain(question, chat_log=None):
    """
    Given a question, generates a response using OpenAI GPT-3 model and updates the chat log file.
    """
    # Read the chat log from the file
    with open(CHAT_LOG_FILE, "r") as f:
        chat_log_template = f.read()

    # Use default chat log template if none is provided
    if chat_log is None:
        chat_log = chat_log_template

    # Construct prompt with question and chat log history
    prompt = f'{chat_log}You: {question}\nMrs.D: '

    # Check if prompt is in cache
    with lock:
        if prompt in cache:
            answer = cache[prompt]
        else:
            # Generate response using OpenAI GPT-3 model
            response = completion.create(
                prompt=prompt,
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0)

            # Extract response text
            answer = response.choices[0].text.strip()

            # Add response to cache
            cache[prompt] = answer

    # Write the updated chat log to the file
    chat_log_template_update = chat_log_template + f"\nYou : {question} \nMrs.D : {answer}"
    with open(CHAT_LOG_FILE, "w") as f:
        f.write(chat_log_template_update)

    return answer

# Start chat loop
while True:
    # Listen for user input
    question = MicExecution()

    # Generate response using OpenAI GPT-3 model
    reply = reply_brain(question)

    # Speak response
    Speak(reply)

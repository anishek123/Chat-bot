import speech_recognition as sr
from googletrans import Translator
import subprocess
# import googlemaps

# from Features.map import get_location, display_map
#
# # Set up Google Maps API key
# gmaps = googlemaps.Client(key='your_api_key_here')


# 1- listen: Hindi or English
def Listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You: {query}\n")
        if "open camera" in query.lower():
            subprocess.call("start microsoft.windows.camera:", shell=True)  # open camera app
            return ""
        # elif "open map" in query.lower():
        #     location = get_location()
        #     display_map(location)
        #     return ""
        else:
            return query.lower()

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""


# 2- Translation

def TranslationHinToEng(Text):
    try:
        line = str(Text)
        translate = Translator()
        result = translate.translate(line)
        data = result.text
        print(f"You: {data}.")
        return data

    except Exception as e:
        print(f"Error translating text; {e}")
        return ""


# 3- connect

def MicExecution():
    query = Listen()
    data = TranslationHinToEng(query)
    return data


MicExecution()

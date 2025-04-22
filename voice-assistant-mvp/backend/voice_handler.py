import speech_recognition as sr
from gtts import gTTS
import os
import pyttsx3


def speech_to_text(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)
    return r.recognize_google(audio)

# def speak(text):
#     print(f"[Voice Agent]: {text}")
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 160)  # Speed percent
#     engine.say(text)
#     engine.runAndWait()

# Function to speak text
def speak(text):
    print(f"[Voice Agent]: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(text)
    engine.runAndWait()

def text_to_speech(text):
    print(f"[Voice Agent]: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)  # optional: adjust speech speed
    engine.setProperty('volume', 1.0)  # optional: max volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio)
#         print(f"You said: {command}")
#         return command.lower()
#     except sr.UnknownValueError:
#         print("Could not understand audio.")
#         return ""
#     except sr.RequestError as e:
#         print(f"Could not request results; {e}")
#         return ""
    
    
# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening... Speak now!")
#         recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusting for ambient noise
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio)
#         print(f"You said: {command}")
#         return command.lower()
#     except sr.UnknownValueError:
#         print("Could not understand audio. Please try again.")
#         return ""  # Return empty string if speech is unclear
#     except sr.RequestError as e:
#         print(f"Error in the request; {e}")
#         return ""  # Return empty string in case of API request failure


# Function to listen to voice command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

name = "Assistant"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def process_command(query):
    global name
    if "hello" in query:
        speak(f"Hello! How can I help you?")
    elif "how are you" in query:
        responses = ["I'm doing well, thank you!", "I'm functioning optimally.", "I'm here and ready to assist!"]
        speak(random.choice(responses))
    elif "what time is it" in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time}")
    elif "what day is it" in query or "what is the date" in query:
        date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {date}")
    elif "open google" in query:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    elif "search for" in query:
        query = query.replace("search for", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query}")
    elif "play music" in query or "play a song" in query:
        music_dir = "C:\\path\\to\\your\\music\\directory"
        if os.path.exists(music_dir):
            songs = os.listdir(music_dir)
            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))
                speak(f"Playing {song}")
            else:
                speak("No music files found in the specified directory.")
        else:
            speak("Music directory not found.")
    elif "stop" in query or "exit" in query or "quit" in query:
        speak("Goodbye!")
        exit()
    elif "what is your name" in query:
        speak(f"My name is {name}")
    elif "change your name to" in query:
        new_name = query.replace("change your name to", "").strip()
        if new_name:
            name = new_name
            speak(f"My name is now {name}")
        else:
            speak("Please provide a name.")
    else:
        speak("Sorry, I don't understand that command.")

speak("Initializing voice assistant...")
while True:
    query = get_audio()
    if query:
        process_command(query)
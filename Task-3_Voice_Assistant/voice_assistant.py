import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sounddevice as sd
import numpy as np

# -------- TEXT TO SPEECH --------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# -------- SPEECH INPUT --------
def listen():
    r = sr.Recognizer()
    duration = 5  # seconds to listen
    fs = 44100

    device_id = 1  # Your Microphone (Realtek)

    print("Listening...")
    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='int16',
        device=device_id
    )
    sd.wait()

    audio_data = np.squeeze(recording)
    audio = sr.AudioData(audio_data.tobytes(), fs, 2)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Speech service is not available")
        return ""

# -------- FEATURES --------
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak("The time is " + current_time)

def tell_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak("Today's date is " + current_date)

# -------- MAIN --------
speak("Hello. I am your voice assistant.")

while True:
    command = listen()

    if command == "":
        speak("Sorry, I did not understand.")
        continue

    # Greeting
    if "hello" in command:
        speak("Hello! How can I help you?")

    # Time
    elif "time" in command:
        tell_time()

    # Date
    elif "date" in command:
        tell_date()

    # Search (Improved Version)
    elif "search" in command:
        speak("What should I search for?")
        query = listen()

        if query != "":
            speak("Searching for " + query)
            webbrowser.open("https://www.google.com/search?q=" + query)
        else:
            speak("I did not hear the search topic.")

    # Exit
    elif "exit" in command or "stop" in command or "quit" in command:
        speak("Goodbye. Have a nice day.")
        break

    else:
        speak("Sorry, I did not understand.")

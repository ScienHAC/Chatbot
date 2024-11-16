from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import os
import sounddevice as sd
import numpy as np
from scipy.io import wavfile

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def record_audio(filename, duration=5, fs=44100):
    print("Listening...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs,
                        channels=1, dtype=np.int16)
    sd.wait()
    wavfile.write(filename, fs, audio_data)
    return filename


def listen():
    recognizer = sr.Recognizer()
    audio_filename = "temp_audio.wav"
    record_audio(audio_filename)

    with sr.AudioFile(audio_filename) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
            print(f"You said: {text}")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-pro-002")

            response = model.generate_content(
                f"Answer in English and Hindi Both: {text}")

            if response and response.text:
                return response.text, text
            else:
                print("No response received from the model.")
                speak("Sorry, I didn't receive any response.")
                return None
        except sr.UnknownValueError:
            # If speech is unintelligible
            print("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            # If there's a request error with the speech recognition service
            print("Sorry, the speech recognition service is not available.")
            speak("Sorry, the speech recognition service is not available.")
            return None


def main():
    """Main function to run the voice assistant."""
    speak("Hello, how can I help you?")
    while True:
        command = listen()  # Listen for the user's command
        if command:
            # Process recognized speech
            if "hello" in command[1].lower():
                speak("Hello! How can I assist you today?")
            elif "stop" in command[1].lower():
                speak("Goodbye!")
                break
            else:
                speak(command[0])


if __name__ == "__main__":
    main()

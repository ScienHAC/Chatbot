from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import os
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import webbrowser
import subprocess

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

            # Sanitize input by removing special characters
            sanitized_text = ''.join(
                char for char in text if char.isalnum() or char.isspace())

            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
            print(f"You said: {sanitized_text}")

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-pro-002")

            # Refined prompt for shorter, conversational response
            response = model.generate_content(
                f"Answer briefly and naturally as if in a chatbot conversation: {sanitized_text}")

            if response and response.text:
                return response.text.strip(), sanitized_text
            else:
                print("No response received from the model.")
                speak("Sorry, I didn't receive any response.")
                return None
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
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
            elif "open youtube" in command[1].lower():
                speak("Opening YouTube.")
                webbrowser.open("https://www.youtube.com")
                break
            elif "open chrome" in command[1].lower():
                speak("Opening Chrome.")
                try:
                    # Replace the path with the correct path to Chrome on your system
                    subprocess.Popen(
                        [r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
                    break
                except FileNotFoundError:
                    speak("Chrome is not found on your system.")
            else:
                speak(command[0])


if __name__ == "__main__":
    main()

from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import os
# import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()


def speak(text):
    """This function takes text as input and speaks it."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """This function listens to the microphone and returns recognized speech as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(
            source)  # Adjusts for ambient noise
        audio = recognizer.listen(source)
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
            print(f"You said: {text}")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"{text}? avoid read this stars '*' also try to answer in hindi but written in english")
            # response.text = response.text.replace("*", "")
            return response.text, text
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

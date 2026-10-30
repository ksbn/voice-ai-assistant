import os
import speech_recognition as sr
import pyttsx3
from groq import Groq

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("Missing GROQ_API_KEY environment variable!")

client = Groq(api_key=api_key)
recognizer = sr.Recognizer()

def say(text: str):
    print(f"Assistant: {text}")
    try:
        speaker = pyttsx3.init()
        try:
            voices = speaker.getProperty('voices')
            if voices:
                for voice in voices: # type: ignore
                    if voice.name and ("дэниэл" in voice.name.lower() or "daniel" in voice.name.lower()):
                        speaker.setProperty('voice', voice.id) 
                        break
        except Exception:
            pass

        speaker.setProperty('rate', 160)
        speaker.setProperty('volume', 1.0)
        speaker.say(text)
        speaker.runAndWait()
        
    except Exception as e:
        print(f"TTS Error: {e}")

def listen() -> str: # type: ignore
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except Exception:
            return ""
    
    try:
        google_recognizer = getattr(recognizer, "recognize_google", None)
        if google_recognizer is None:
            raise sr.RequestError("Google recognition is unavailable")

        text = google_recognizer(audio, language="en-GB")
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("No connection with recognition service")
        return ""

chat_history: list[dict[str, str]] = [
    {
        'role': 'system', 
        'content': 'You are Daniel, a friendly, concise AI voice assistant. Keep answers short (1-2 sentences).'
    }
]

def run_assistant():
    say("Hi! I'm Daniel. What's on your mind?")

    while True:
        command = listen()
        if not command:
            continue
            
        if any(word in command for word in ["bye", "goodbye", "exit", "quit"]):
            say("See you later!")
            break

        chat_history.append({'role': 'user', 'content': command})

        print("Thinking...")
        try:
         
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=chat_history # pyright: ignore[reportArgumentType]
            )
            ai_reply = completion.choices[0].message.content
            
            chat_history.append({'role': 'assistant', 'content': ai_reply}) # type: ignore
            if ai_reply:
                say(ai_reply)
            
        except Exception as e:
            print(f"Groq API Error: {e}")
            say("Sorry, I had trouble thinking of a response.")

if __name__ == "__main__":
    run_assistant()
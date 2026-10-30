import speech_recognition as sr
import pyttsx3
import ollama

recognizer = sr.Recognizer()

def say(text: str):
    print(f"Assistant: {text}")
    try:
        speaker = pyttsx3.init()

        try:
            voices = speaker.getProperty('voices')
            if voices:
                for voice in voices:
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

def listen() -> str:
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except Exception as e:
            return ""
    
    try:
        text = recognizer.recognize_google(audio, language="en-GB")
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("No connection with service")
        return ""

chat_history : list[dict[str, str]] = [
    {
        'role': 'system', 
        'content': 'You are Daniel, a friendly, concise AI voice assistant. Keep answers short (1-2 sentences).'
    }
]

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
        response = ollama.chat(
            model='llama3.2', 
            messages=chat_history
        )
        ai_reply = response.message.content if hasattr(response, 'message') else str(response)
        
        chat_history.append({'role': 'assistant', 'content': ai_reply})
        say(ai_reply)
        
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        say("Sorry, I had trouble thinking of a response.")
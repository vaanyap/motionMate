import pyttsx3
import threading

engine = pyttsx3.init()


engine.setProperty('rate', 180)


engine.setProperty('volume', 1.0)

def _speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_feedback(text):
    """Speak feedback in a separate thread (non-blocking)."""
    t = threading.Thread(target=_speak, args=(text,), daemon=True)
    t.start()

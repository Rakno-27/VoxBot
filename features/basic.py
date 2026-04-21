import datetime
import random
from core.speaker import speak

def process(command):
    """Intercepts primitive or simple inquiries locally to drastically preserve external Generative API token quotas."""
    
    # Retrieve local system chronological timestamps
    if "what time is it" in command or "current time" in command or "the time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}.")
        return True
        
    # Retrieve local system date
    if "what is the date" in command or "today's date" in command or "what day is it" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}.")
        return True
        
    # Identity and Politeness Logic
    greetings = ["hello", "hi", "hey", "hey jarvis", "hi jarvis", "hello jarvis", "good morning", "good evening"]
    if any(command == g for g in greetings) or command in greetings:
        resps = ["Hello there! How can I help you?", "Hi! I'm listening.", "Greetings! What's on your mind?"]
        speak(random.choice(resps))
        return True
        
    if "how are you" in command:
        speak("I am functioning at optimal capacity, thank you. How are you?")
        return True
        
    if "who are you" in command:
        speak("I am Jarvis, your personal voice assistant.")
        return True
        
    if "thank you" in command or "thanks jarvis" in command or "thank you jarvis" in command:
        speak("You're very welcome!")
        return True

    return False

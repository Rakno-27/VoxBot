import webbrowser
from core.speaker import speak

def handle_open_site(command):
    sites = {
        "open google": "https://google.com",
        "open facebook": "https://facebook.com",
        "open youtube": "https://youtube.com",
        "open linkedin": "https://linkedin.com"
    }
    
    for phrase, link in sites.items():
        if phrase in command:
            webbrowser.open(link)
            speak(f"Opening {phrase.split(' ')[1]}")
            return True
            
    return False

def process(command, is_offline=False):
    if "open" in command and any(site in command for site in ["google", "facebook", "youtube", "linkedin"]):
        if is_offline:
            speak("I am offline and cannot browse the internet right now.")
            return True
        return handle_open_site(command)
    return False

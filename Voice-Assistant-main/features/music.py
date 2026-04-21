import webbrowser
import musicLibrary
from core.speaker import speak

def handle_play_music(command):
    """Scraps youtube dict hashes against the requested song logic identifier."""
    parts = command.split(" ")
    if len(parts) > 1:
        song = parts[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    else:
        speak("Please specify which song to play.")

def process(command):
    if command.startswith("play"):
        handle_play_music(command)
        return True
    return False

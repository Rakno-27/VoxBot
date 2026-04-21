import os
import time
import pygame
from gtts import gTTS

STATUS_CALLBACK = None

def set_status_callback(func):
    global STATUS_CALLBACK
    STATUS_CALLBACK = func

def speak(text):
    """Converts string format data to speech output through gTTS engine and pygame mixer routines."""
    if STATUS_CALLBACK:
        STATUS_CALLBACK(f"Speaking: {text}")
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')
    except Exception as e:
        print(f"TTS saving error: {e}")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()

        # Wait intelligently while music streams before releasing lock
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Safely shut down streams to circumvent permission locks
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        
        time.sleep(0.1)
        
        try:
            os.remove("temp.mp3")
        except Exception:
            pass
    except Exception as e:
        print(f"Audio playback error: {e}")
        try:
            pygame.mixer.quit()
        except:
            pass

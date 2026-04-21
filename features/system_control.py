import os
import ctypes
from core.speaker import speak

def handle_system_volume(command):
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF
    
    if "up" in command or "increase" in command:
        for _ in range(5):
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
        speak("Turned volume up.")
        return True
    elif "down" in command or "decrease" in command:
        for _ in range(5):
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)
        speak("Turned volume down.")
        return True
    elif "mute" in command:
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
        ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
        speak("Toggled system mute.")
        return True
        
    return False

def handle_open_app(command):
    apps = {
        "notepad": "notepad.exe",
        "chrome": "start chrome",
        "vscode": "code"
    }
    for app_name, app_cmd in apps.items():
        if f"open {app_name}" in command:
            os.system(app_cmd)
            speak(f"Opening {app_name}")
            return True
    return False

def handle_power_state(command):
    from core.listener import listen_for_command
    
    if "shutdown computer" in command or "shutdown pc" in command:
        speak("Are you sure you want to shut down the computer? Please confirm by saying yes or no.")
        response = listen_for_command(speak)
        if response and "yes" in response.lower():
            speak("Shutting down the computer in 15 seconds. Please save your work.")
            os.system("shutdown /s /t 15")
            exit(0)
        else:
            speak("Shutdown sequence cancelled.")
        return True
        
    elif "restart computer" in command or "restart pc" in command:
        speak("Are you sure you want to restart the computer? Please confirm.")
        response = listen_for_command(speak)
        if response and "yes" in response.lower():
            speak("Restarting the computer in 15 seconds.")
            os.system("shutdown /r /t 15")
            exit(0)
        else:
            speak("Restart sequence cancelled.")
        return True
        
    return False

def process(command, is_offline=False):
    if "shutdown computer" in command or "shutdown pc" in command or "restart computer" in command or "restart pc" in command:
        return handle_power_state(command)
    if "volume" in command or "mute" in command:
        return handle_system_volume(command)
    if "open" in command and any(app in command for app in ["notepad", "chrome", "vscode"]):
        return handle_open_app(command)
    return False

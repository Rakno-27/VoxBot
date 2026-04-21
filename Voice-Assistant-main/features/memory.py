import os
from core.speaker import speak

reminders = []

def handle_create_note(command):
    content = ""
    if "make a note that" in command:
        content = command.split("make a note that")[1].strip()
    elif "write a note" in command:
        content = command.split("write a note")[1].strip()
    elif "note" in command:
        parts = command.split("note", 1)
        if len(parts) > 1:
            content = parts[1].strip()
            
    if content:
        with open("notes.txt", "a") as f:
            f.write(f"- {content}\n")
        speak("I have saved that note.")
        return True
    else:
        speak("What would you like the note to say?")
        return True

def handle_read_notes():
    if not os.path.exists("notes.txt"):
        speak("You do not have any saved notes.")
        return True
        
    try:    
        with open("notes.txt", "r") as f:
            notes = f.readlines()
            
        if not notes:
            speak("Your notes file is empty.")
        else:
            speak("Here are your saved notes.")
            for note in notes:
                speak(note)
    except Exception as e:
        print(f"Error reading notes: {e}")
        speak("I am unable to read your notes right now.")
    return True

def handle_set_reminder(command):
    content = ""
    if "remind me to" in command:
        content = command.split("remind me to")[1].strip()
    elif "remind me that" in command:
        content = command.split("remind me that")[1].strip()
        
    if content:
        reminders.append(content)
        speak(f"I will remind you to {content}.")
    else:
        speak("What would you like to be reminded about?")
    return True

def handle_read_reminders():
    if not reminders:
        speak("You have no active reminders.")
    else:
        speak(f"You have {len(reminders)} reminders.")
        for r in reminders:
            speak(r)
    return True

def process(command):
    if "remind me" in command:
        return handle_set_reminder(command)
    if any(q in command for q in ["what are my reminders", "read reminders", "check reminders"]):
        return handle_read_reminders()
    if "make a note" in command or "write a note" in command:
        return handle_create_note(command)
    if "read notes" in command or "what are my notes" in command:
        return handle_read_notes()
    return False

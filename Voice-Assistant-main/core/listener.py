import speech_recognition as sr

recognizer = sr.Recognizer()

STATUS_CALLBACK = None
COMMAND_CALLBACK = None

def set_callbacks(status_func, cmd_func):
    global STATUS_CALLBACK, COMMAND_CALLBACK
    STATUS_CALLBACK = status_func
    COMMAND_CALLBACK = cmd_func

def _update_status(msg):
    if STATUS_CALLBACK:
        STATUS_CALLBACK(msg)

def _update_command(cmd):
    if COMMAND_CALLBACK:
        COMMAND_CALLBACK(cmd)

def listen_for_wake_word():
    """Isolates the passive wake word detection into a standalone logic check."""
    try:
        with sr.Microphone() as source:
            _update_status("Listening for wake word...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=1)
        _update_status("Processing wake word...")
        
        try:
            word = recognizer.recognize_google(audio).lower()
        except sr.RequestError:
            word = recognizer.recognize_sphinx(audio).lower()
            
        return word == "jarvis"
    except (sr.WaitTimeoutError, sr.UnknownValueError):
        pass
    except Exception as e:
        print(f"Unexpected wake-word error: {e}")
    return False

def listen_for_command(speak_fallback):
    """Isolates the primary active command interpreter."""
    try:
        with sr.Microphone() as source:
            _update_status("Listening for command...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        _update_status("Processing command...")
        
        try:
            cmd = recognizer.recognize_google(audio)
            _update_command(cmd)
            return cmd
        except sr.RequestError:
            _update_status("Offline Mode Mapping...")
            try:
                cmd = recognizer.recognize_sphinx(audio)
                _update_command(f"Offline: {cmd}")
                return cmd
            except sr.UnknownValueError:
                pass
            except Exception as e:
                speak_fallback("Offline voice recognition physically failed. Microphone unlinked.")
                print(e)
                return None
                
    except sr.WaitTimeoutError:
        pass
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

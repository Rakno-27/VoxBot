import os
import threading
import tkinter as tk
import time

# Feature Imports
from core.speaker import speak, set_status_callback as speaker_set_callback
from core.listener import listen_for_wake_word, listen_for_command, set_callbacks as listener_set_callbacks
from core.brain import fetch_ai_response
import pkgutil
import importlib
import features

# Dynamically auto-load all scripts inside the features package
loaded_plugins = []
for _, module_name, _ in pkgutil.iter_modules(features.__path__):
    module = importlib.import_module(f"features.{module_name}")
    loaded_plugins.append(module)

# GUI Global State
assistant_active = False
status_var = None
command_var = None
IS_OFFLINE = False

def network_monitor():
    global IS_OFFLINE
    import socket
    while True:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            if IS_OFFLINE:
                update_status("Connection Restored")
            IS_OFFLINE = False
        except OSError:
            if not IS_OFFLINE:
                update_status("Offline Mode Active")
            IS_OFFLINE = True
        time.sleep(10)

def update_status(msg):
    print(msg)
    if status_var:
        status_var.set(msg)

def update_command(cmd):
    if command_var:
        command_var.set(f"Last Command: {cmd}")

# Inject Callbacks into modular architecture
speaker_set_callback(update_status)
listener_set_callbacks(update_status, update_command)

def processCommand(c):
    """Core master controller routing explicit traffic to correct modular handlers."""
    command = c.lower()
    
    # 1. Exit Commands
    if command in ["exit", "stop", "shutdown", "quit"]:
        speak("Shutting down. Goodbye!")
        os._exit(0)
        
    # 2. Dynamic Plugin Execution Loop
    for plugin in loaded_plugins:
        if hasattr(plugin, "process"):
            try:
                handled = plugin.process(command, is_offline=IS_OFFLINE)
            except TypeError:
                handled = plugin.process(command)
                
            if handled:
                return
        
    # 3. Generative AI Fallback
    if IS_OFFLINE:
        speak("Offline mode active. I cannot process advanced commands right now.")
    else:
        output = fetch_ai_response(c)
        speak(output)

def start_voice_loop():
    update_status("Initializing System...")
    speak("Initializing Jarvis")
    while True:
        if assistant_active:
            if listen_for_wake_word():
                speak("Ya")
                command = listen_for_command(speak)
                if command:
                    processCommand(command)
        else:
            time.sleep(1)

def run_gui():
    global status_var, command_var, assistant_active
    
    root = tk.Tk()
    root.title("Jarvis Voice Assistant")
    root.geometry("400x250")
    root.configure(bg="#1e1e1e")
    
    status_var = tk.StringVar()
    status_var.set("System Offline")
    
    command_var = tk.StringVar()
    command_var.set("Last Command: None")
    
    def toggle_assistant():
        global assistant_active
        assistant_active = not assistant_active
        if assistant_active:
            toggle_btn.config(text="Stop Jarvis", bg="#ff4c4c")
            update_status("Microphone Enabled")
        else:
            toggle_btn.config(text="Start Jarvis", bg="#4caf50")
            update_status("System Offline (Paused)")
    
    # UI Elements
    title_lbl = tk.Label(root, text="🤖 JARVIS", font=("Arial", 20, "bold"), fg="#00e5ff", bg="#1e1e1e")
    title_lbl.pack(pady=10)
    
    status_lbl = tk.Label(root, textvariable=status_var, font=("Arial", 12, "italic"), fg="#ffffff", bg="#1e1e1e")
    status_lbl.pack(pady=5)
    
    cmd_lbl = tk.Label(root, textvariable=command_var, font=("Arial", 10), fg="#b0bec5", bg="#1e1e1e")
    cmd_lbl.pack(pady=15)
    
    toggle_btn = tk.Button(root, text="Start Jarvis", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", borderwidth=0, padx=20, pady=10, cursor="hand2", command=toggle_assistant)
    toggle_btn.pack(pady=10)
    
    def on_closing():
        root.destroy()
        os._exit(0)
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start threads
    t = threading.Thread(target=start_voice_loop, daemon=True)
    t.start()
    
    t2 = threading.Thread(target=network_monitor, daemon=True)
    t2.start()
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()

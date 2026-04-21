# Jarvis AI Voice Assistant 🤖🎙️

A robust, modular, production-ready Voice Assistant powered by Python. Built with a drag-and-drop plugin architecture, a real-time Tkinter GUI dashboard, offline fallback support via PocketSphinx, and deep OS-level system integration.

---

## 🌟 Features

| Category | Commands |
|---|---|
| **Wake Word** | Say `"Jarvis"` to activate |
| **Greetings** | `"Hello"`, `"How are you"`, `"Who are you"`, `"Thank you"` |
| **Date & Time** | `"What time is it"`, `"What is the date"` |
| **Music** | `"Play [song name]"` — streams via browser from `musicLibrary.py` |
| **News** | `"Tell me the news"`, `"Tech news"`, `"Sports news"`, `"Business news"` |
| **Browser** | `"Open Google"`, `"Open YouTube"`, `"Open Facebook"`, `"Open LinkedIn"` |
| **Apps** | `"Open Notepad"`, `"Open Chrome"`, `"Open VSCode"` |
| **Volume** | `"Volume up"`, `"Volume down"`, `"Mute"` |
| **Power** | `"Shutdown computer"`, `"Restart computer"` *(with confirmation)* |
| **Notes** | `"Make a note that [text]"`, `"Read my notes"` |
| **Reminders** | `"Remind me to [task]"`, `"Read reminders"` |
| **AI Fallback** | Any complex query → sent to OpenAI `gpt-3.5-turbo` |
| **Exit** | `"Exit"`, `"Stop"`, `"Quit"` |

---

## 🏗️ Project Structure

```
Voice-Assistant-main/
│
├── main.py                  # Entry point: Tkinter GUI + plugin router
│
├── core/                    # Core engine modules
│   ├── listener.py          # Microphone input & speech recognition
│   ├── speaker.py           # gTTS + pygame audio output
│   └── brain.py             # OpenAI API integration
│
├── features/                # Auto-loaded plugin modules
│   ├── basic.py             # Local: greetings, time, date (no API usage)
│   ├── browser.py           # Website navigation
│   ├── music.py             # Music playback via musicLibrary
│   ├── news.py              # NewsAPI headlines by category
│   ├── memory.py            # Notes & reminders
│   └── system_control.py    # Volume, app launching, shutdown/restart
│
├── utils/                   # Utility helpers (extensible)
│
├── musicLibrary.py          # Song name → YouTube URL dictionary
├── requirements.txt         # Python dependencies
└── .env                     # API keys (not committed to version control)
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.9+
- A working microphone
- OS microphone permissions granted to the terminal / Python

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Full dependency list (`requirements.txt`):**
```
SpeechRecognition==3.10.4
pyttsx3==2.90
pygame==2.6.1
requests==2.31.0
gTTS==2.5.1
openai==1.30.1
python-dotenv==1.0.1
pocketsphinx==5.0.4
```

> **Note:** `pocketsphinx` is required for offline speech recognition fallback when internet is unavailable.

### 3. Configure Environment Keys
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_key_here
NEWS_API_KEY=your_newsapi_key_here
```

- Get your OpenAI key at: https://platform.openai.com/api-keys
- Get your NewsAPI key at: https://newsapi.org/register

### 4. Run
```bash
python main.py
```

---

## 🖥️ GUI Dashboard

The assistant launches a dark-mode Tkinter desktop window with:

- **🤖 JARVIS** title header
- **Live status indicator** — updates in real-time: `Listening...` → `Processing...` → `Speaking...`
- **Last command display** — shows what was heard after each command
- **Start / Stop toggle button** — enables or disables the microphone loop without closing the app

The voice loop runs on a **background daemon thread**, keeping the GUI fully responsive at all times.

---

## 🔌 Plugin System

All features in the `features/` folder are **auto-discovered and loaded at startup** using Python's `pkgutil` + `importlib`. No manual registration required.

**To add a new feature:**

1. Create a new file inside `features/`, e.g. `features/weather.py`
2. Implement a `process(command, is_offline=False)` function:

```python
# features/weather.py
from core.speaker import speak

def process(command, is_offline=False):
    if "weather" in command:
        if is_offline:
            speak("I'm offline and cannot fetch weather data.")
            return True
        speak("It's sunny today!")  # Replace with real API call
        return True
    return False
```

3. Save the file. Jarvis will load it automatically on next startup.

> Return `True` if your plugin handled the command, `False` to pass to the next plugin.

---

## 📡 Offline Mode

A background network monitor pings `8.8.8.8` (Google DNS) every 10 seconds.

- **If offline:**
  - GUI status updates to `"Offline Mode Active"`
  - Internet-dependent features (News, OpenAI) are blocked with a friendly message
  - Local features remain fully functional: time, date, greetings, volume, notes, reminders, app launching
  - Speech recognition falls back to **PocketSphinx** (local, no internet required)

- **When reconnected:**
  - Status updates to `"Connection Restored"` automatically

---

## 🛡️ Safety Features

- **Shutdown/Restart confirmation**: Jarvis asks *"Are you sure?"* and listens for a *"Yes"* before executing any power command. Saying anything else cancels the action.
- **API timeouts**: All external requests have timeout limits to prevent hangs.
- **Speech recognition timeouts**: `timeout=5` and `phrase_time_limit=5` prevent the microphone from blocking indefinitely.
- **Graceful exit**: Saying `"Exit"` or `"Quit"` cleanly terminates all threads and the GUI.

---

## 📝 Usage Examples

```
User: "Jarvis"
Jarvis: "Ya"

User: "What time is it?"
Jarvis: "The time is 4:30 PM."

User: "Play blinding lights"
Jarvis: [Opens YouTube link in browser]

User: "Tell me the tech news"
Jarvis: [Reads top 5 technology headlines]

User: "Shutdown computer"
Jarvis: "Are you sure you want to shut down? Say yes or no."
User: "Yes"
Jarvis: "Shutting down in 15 seconds. Please save your work."

User: "Remind me to drink water"
Jarvis: "I will remind you to drink water."

User: "Exit"
Jarvis: "Shutting down. Goodbye!"
```

---

## ⚠️ Limitations

- **PocketSphinx accuracy**: Offline voice recognition is less accurate than Google STT for conversational speech. Simple commands (volume, mute) work well.
- **Reminders are in-memory**: Reminders are lost when the app is closed. Persist them to `reminders.json` for long-term storage.
- **News API**: Hardcoded to `country=in` (India). Edit `features/news.py` to change the region.
- **Music Library**: Songs must be manually added to `musicLibrary.py` as `name → URL` pairs.

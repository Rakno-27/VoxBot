# VoxBot 🤖🎙️ — AI Voice Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-GPT--3.5-green?style=for-the-badge&logo=openai" />
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

**VoxBot** is a modular, production-ready AI voice assistant for Windows — wake-word activated, plugin-extensible, and GUI-driven. It integrates OpenAI GPT, NewsAPI, OS-level system controls, and offline speech recognition fallback via PocketSphinx.

---

## ✨ Features

| Category | Voice Commands |
|---|---|
| 🎙️ **Wake Word** | Say `"Jarvis"` to activate |
| 👋 **Greetings** | `"Hello"`, `"How are you"`, `"Who are you"`, `"Thank you"` |
| 🕐 **Date & Time** | `"What time is it"`, `"What is the date"` |
| 🎵 **Music** | `"Play [song name]"` — opens YouTube via browser |
| 📰 **News** | `"Tell me the news"`, `"Tech news"`, `"Sports news"`, `"Business news"` |
| 🌐 **Browser** | `"Open Google"`, `"Open YouTube"`, `"Open Facebook"`, `"Open LinkedIn"` |
| 💻 **Apps** | `"Open Notepad"`, `"Open Chrome"`, `"Open VSCode"` |
| 🔊 **Volume** | `"Volume up"`, `"Volume down"`, `"Mute"` |
| ⚡ **Power** | `"Shutdown computer"`, `"Restart computer"` *(voice confirmation required)* |
| 📝 **Notes** | `"Make a note that [text]"`, `"Read my notes"` |
| 🔔 **Reminders** | `"Remind me to [task]"`, `"Read reminders"`, `"Check reminders"` |
| 🤖 **AI Fallback** | Any complex query → routed to OpenAI `gpt-3.5-turbo` |
| 🚪 **Exit** | `"Exit"`, `"Stop"`, `"Quit"` |

---

## 🏗️ Project Structure

```
Voice-Assistant-main/
│
├── main.py                    # Entry point — Tkinter GUI + plugin router
│
├── core/                      # Core engine (voice I/O + AI brain)
│   ├── __init__.py
│   ├── listener.py            # Microphone input & speech recognition (Google + PocketSphinx)
│   ├── speaker.py             # gTTS + pygame text-to-speech output
│   └── brain.py               # OpenAI GPT-3.5 API integration
│
├── features/                  # Auto-loaded plugin modules
│   ├── __init__.py
│   ├── basic.py               # Local: greetings, time, date (zero API usage)
│   ├── browser.py             # Website navigation via webbrowser
│   ├── music.py               # Music playback via musicLibrary dictionary
│   ├── news.py                # NewsAPI category-based headlines
│   ├── memory.py              # Notes (notes.txt) & in-memory reminders
│   └── system_control.py     # Volume, app launching, shutdown/restart
│
├── utils/                     # Utility helpers (reserved for future use)
│   └── __init__.py
│
├── musicLibrary.py            # Song → YouTube URL dictionary
├── requirements.txt           # Python dependencies
├── .env                       # 🔑 API keys (NOT committed to git)
├── .gitignore
├── LICENSE
└── CONTRIBUTING.md
```

---

## ⚙️ Installation

### Prerequisites
- Python **3.9+**
- A working **microphone**
- Windows OS (for system controls via `ctypes`)
- Microphone permissions granted to your terminal / Python

### Step 1 — Clone the repository
```bash
git clone https://github.com/Rakno-27/VoxBot.git
cd VoxBot/Voice-Assistant-main
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** If `pyaudio` fails to install on Windows, use the pre-compiled wheel:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Step 3 — Configure API keys
Create a `.env` file in the `Voice-Assistant-main/` directory:
```env
OPENAI_API_KEY=your_openai_key_here
NEWS_API_KEY=your_newsapi_key_here
```

- 🔑 OpenAI key: https://platform.openai.com/api-keys
- 🔑 NewsAPI key: https://newsapi.org/register

### Step 4 — Run
```bash
python main.py
```

---

## 🖥️ GUI Dashboard

VoxBot launches a **dark-mode Tkinter desktop window** featuring:

- A live **status indicator** — transitions in real-time: `Listening...` → `Processing...` → `Speaking...`
- A **last command** display showing exactly what was heard
- A **Start / Stop toggle button** — enables or pauses the microphone without closing the app

The voice loop runs on a **background daemon thread**, keeping the GUI fully responsive at all times.

---

## 🔌 Plugin System

All files inside `features/` are **auto-discovered and loaded at startup** using Python's `pkgutil` + `importlib`. No manual registration needed.

### Adding a New Feature

1. Create a file inside `features/`, e.g. `features/weather.py`
2. Implement a `process(command, is_offline=False)` function:

```python
# features/weather.py
from core.speaker import speak

def process(command, is_offline=False):
    if "weather" in command:
        if is_offline:
            speak("I'm offline and cannot fetch weather data.")
            return True
        speak("Fetching weather...")   # Replace with real API call
        return True
    return False
```

3. Save the file. VoxBot will load it automatically on the next startup.

> Return `True` if your plugin handled the command, `False` to pass control to the next plugin.

---

## 📡 Offline Mode

A background thread pings `8.8.8.8` (Google DNS) every 10 seconds to detect connectivity.

| State | Behaviour |
|---|---|
| **No internet** | GUI shows `"Offline Mode Active"` |
| **No internet** | News & OpenAI features blocked with a clear message |
| **No internet** | Local features stay fully active (time, notes, volume, apps) |
| **No internet** | Speech recognition falls back to **PocketSphinx** (local) |
| **Reconnected** | GUI shows `"Connection Restored"` automatically |

---

## 🛡️ Safety Features

- **Power confirmation** — Shutdown/Restart require a spoken *"Yes"* confirmation before executing
- **API timeouts** — All HTTP requests have timeout guards to prevent hangs
- **STT timeouts** — `timeout=5` + `phrase_time_limit=5` prevent infinite microphone blocking
- **Graceful exit** — `"Exit"` / `"Quit"` cleanly terminates all threads and the GUI

---

## 📝 Usage Examples

```
You:    "Jarvis"
VoxBot: "Ya"

You:    "What time is it?"
VoxBot: "The time is 4:30 PM."

You:    "Play blinding lights"
VoxBot: [Opens YouTube in browser]

You:    "Tell me the tech news"
VoxBot: [Reads 5 technology headlines aloud]

You:    "Shutdown computer"
VoxBot: "Are you sure you want to shut down? Say yes or no."
You:    "Yes"
VoxBot: "Shutting down in 15 seconds. Please save your work."

You:    "Remind me to drink water"
VoxBot: "I will remind you to drink water."

You:    "Exit"
VoxBot: "Shutting down. Goodbye!"
```

---

## 🚀 Future Improvements

- [ ] **Weather plugin** — integrate OpenWeatherMap API
- [ ] **Persistent reminders** — save to `reminders.json` instead of in-memory only
- [ ] **Calendar integration** — Google Calendar API for event scheduling
- [ ] **Custom wake word** — replace "Jarvis" with a trainable Porcupine/Snowboy model
- [ ] **Multi-language support** — gTTS supports 50+ languages
- [ ] **Cross-platform** — extend OS controls to macOS/Linux
- [ ] **Conversation history** — maintain multi-turn context in OpenAI calls
- [ ] **Settings UI** — GUI panel for toggling features and managing API keys

---

## ⚠️ Known Limitations

- **PocketSphinx accuracy** — Offline STT is less accurate than Google STT for natural speech; simple commands (volume, mute) work reliably
- **In-memory reminders** — Reminders reset on app close (fix: migrate to `reminders.json`)
- **News region** — Hardcoded to `country=in` (India); edit `features/news.py` to change
- **Music library** — Songs must be manually added to `musicLibrary.py` as `name → URL` pairs
- **Windows-only** — `ctypes` volume control and app spawning are Windows-specific

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

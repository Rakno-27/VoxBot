# Contributing to VoxBot 🤝

Thank you for your interest in contributing! VoxBot is built on a plugin architecture — adding features is simple and self-contained.

---

## 🚀 Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/VoxBot.git
   cd VoxBot/Voice-Assistant-main
   ```
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/my-new-plugin
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure your `.env`** with your own API keys (see README)

---

## 🔌 Adding a New Plugin

The easiest way to contribute is by adding a new feature plugin.

1. Create a file in `features/`, e.g. `features/weather.py`
2. Implement the standard `process()` interface:

```python
from core.speaker import speak

def process(command, is_offline=False):
    """
    Handle voice commands related to weather.
    Returns True if this plugin handled the command, False otherwise.
    """
    if "weather" in command:
        if is_offline:
            speak("I'm offline and cannot fetch weather data.")
            return True
        # Your logic here
        speak("It looks sunny today!")
        return True
    return False
```

3. VoxBot will auto-discover and load it on next startup — no changes to `main.py` needed.

---

## 📋 Contribution Guidelines

- **Keep it focused** — each plugin should do one thing well
- **Always handle `is_offline`** — check the flag before making any network requests
- **Return booleans correctly** — `True` = handled, `False` = pass to next plugin
- **Use `core.speaker.speak()`** for all voice output — do not print to console as output
- **No hardcoded secrets** — use `.env` and `python-dotenv` for all API keys
- **Follow existing code style** — snake_case, clear docstrings, try/except blocks on all I/O

---

## 🐛 Reporting Bugs

Please open a GitHub Issue with:
- What you said / typed as the command
- What VoxBot did (or didn't do)
- Any error messages from the terminal
- Your Python version and OS

---

## 📬 Pull Requests

- Keep PRs small and focused on one change
- Add a clear description of what the PR does
- Test your change locally before submitting
- Link any related issues in the PR description

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

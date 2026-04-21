"""
VoxBot Test Suite
-----------------
Validates core command routing by mocking speak and browser output.
Run from the Voice-Assistant-main/ directory:
    python test_suite.py
"""
import sys
import os

# Ensure imports resolve from project root
sys.path.insert(0, os.path.dirname(__file__))

# Patch speaker before importing main (avoids audio hardware requirement)
import core.speaker as speaker_module
speaker_module.speak = lambda txt: print(f"[SPEAK]: {txt}")

import main

# Also mock browser opens
import webbrowser
webbrowser.open = lambda url: print(f"[BROWSER]: {url}")

print("\n=== VoxBot Validation Test Suite ===\n")

print("--- 1. Play command without song name (should not crash) ---")
main.processCommand("play")

print("\n--- 2. Play command with song name ---")
main.processCommand("play blinding")

print("\n--- 3. News command ---")
main.processCommand("news")

print("\n--- 4. Time command (local, no API) ---")
main.processCommand("what time is it")

print("\n--- 5. Greeting command (local, no API) ---")
main.processCommand("hello")

print("\n--- 6. Exit command ---")
try:
    main.processCommand("exit")
except SystemExit:
    print("[PASS]: SystemExit raised correctly on exit command")

print("\n=== All tests completed ===")

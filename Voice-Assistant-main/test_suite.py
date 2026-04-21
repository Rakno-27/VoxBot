import main

# Mock core output dependencies
main.speak = lambda txt: print(f"[MOCK SPEAK Output]: {txt}")
main.webbrowser.open = lambda url: print(f"[MOCK BROWSER Output]: Opening URL -> {url}")

print("\n=== Validation Test Suite ===")

print("\n--- 1. Testing PLAY without song (Should NOT crash) ---")
main.processCommand("play")

print("\n--- 2. Testing PLAY with song ---")
main.processCommand("play blinding")

print("\n--- 3. Testing NEWS (With missing key / Mocked) ---")
# Simulating missing key or fallback properly
main.processCommand("news")

print("\n--- 4. Testing EXIT mechanism ---")
try:
    main.processCommand("exit")
except SystemExit:
    print("[MOCK SYSTEM EXIT VERIFIED]")

print("\n=== End-to-End simulation completed successfully ===")

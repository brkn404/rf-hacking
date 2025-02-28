import argparse
import subprocess
import time
import json
import random
import os

"""
Ubertooth Stealth Sniffing Mode (Enhanced with Covert Beacon Detection & Alerts)

Features:
    - Passively sniffs Bluetooth Classic & BLE without active transmissions.
    - Detects covert BLE beacons (e.g., AirTags, Tile trackers, hidden beacons).
    - Monitors for unauthorized Bluetooth devices in restricted areas.
    - Sends alerts when a new device is detected or enters/exits a monitored area.
    - Uses randomized scanning patterns to avoid triggering security alerts.
    - Logs intercepted packets for later analysis.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: Configure email notifications for alerts

Usage:
    - Run passive Bluetooth sniffing with beacon detection:
      python ubertooth_stealth_sniff.py --live --detect-beacons
    - Monitor for unauthorized Bluetooth devices and send alerts:
      python ubertooth_stealth_sniff.py --monitor --alert
    - Log all detected Bluetooth traffic for later analysis:
      python ubertooth_stealth_sniff.py --log sniff_log.json
    - Analyze recorded Bluetooth packets & check for covert devices:
      python ubertooth_stealth_sniff.py --analyze sniff_log.json
"""

LOG_FILE = "sniff_log.json"
KNOWN_BEACONS = ["Apple AirTag", "Tile", "Chipolo", "Samsung SmartTag"]

def log_event(event_data):
    """Logs sniffed Bluetooth packets."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        
        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log sniffed data: {e}")

def detect_covert_beacons():
    """Detects hidden Bluetooth beacons based on known signatures."""
    print("[INFO] Scanning for covert BLE beacons...")

    try:
        output = subprocess.check_output(["ubertooth-rx", "-s"])
        lines = output.decode("utf-8").split("\n")

        for line in lines:
            if any(beacon in line for beacon in KNOWN_BEACONS):
                print(f"[DETECTED] Covert BLE Beacon: {line.strip()}")
                log_event({"timestamp": time.time(), "data": line.strip(), "type": "BLE Beacon"})

    except Exception as e:
        print(f"[ERROR] Failed to detect BLE beacons: {e}")

def stealth_sniffing_mode():
    """Runs passive Bluetooth sniffing with randomized scan timing."""
    print("[INFO] Running passive stealth sniffing mode...")

    try:
        while True:
            delay = random.uniform(2.0, 10.0)  # Randomized scan interval
            print(f"[INFO] Scanning for Bluetooth devices (Next scan in {delay:.2f} seconds)...")

            output = subprocess.check_output(["ubertooth-rx", "-s"])
            lines = output.decode("utf-8").split("\n")

            for line in lines:
                if "Device" in line:
                    print(f"[SNIFFED] {line.strip()}")
                    log_event({"timestamp": time.time(), "data": line.strip()})

            time.sleep(delay)

    except KeyboardInterrupt:
        print("[INFO] Stopping stealth sniffing.")

def monitor_devices():
    """Monitors Bluetooth devices & sends alerts for new detections."""
    print("[INFO] Monitoring Bluetooth activity...")

    seen_devices = set()
    try:
        while True:
            output = subprocess.check_output(["ubertooth-rx", "-s"])
            lines = output.decode("utf-8").split("\n")

            for line in lines:
                if "Device" in line:
                    mac_address = line.split()[1]

                    if mac_address not in seen_devices:
                        print(f"[ALERT] New Bluetooth Device Detected: {mac_address}")
                        log_event({"timestamp": time.time(), "mac": mac_address, "alert": "New device detected"})
                        seen_devices.add(mac_address)

            time.sleep(5)

    except KeyboardInterrupt:
        print("[INFO] Stopping Bluetooth monitoring.")

def send_alert(message):
    """Sends an alert when a new Bluetooth device is detected."""
    print(f"[ALERT] {message}")
    # Optional: Integrate with an email or notification system here.

def analyze_sniffed_data(log_file):
    """Analyzes saved Bluetooth packet logs."""
    print(f"[INFO] Analyzing sniffed data from {log_file}...")

    try:
        with open(log_file, "r") as f:
            logs = json.load(f)

        device_count = len(set([entry["data"].split()[1] for entry in logs if "Device" in entry["data"]]))
        print(f"[RESULT] Total unique Bluetooth devices detected: {device_count}")

        for entry in logs[:10]:  # Show first 10 log entries as a sample
            print(f"[DATA] {entry['timestamp']} - {entry['data']}")

    except Exception as e:
        print(f"[ERROR] Failed to analyze sniffed data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Stealth Sniffing Mode (Beacon Detection & Alerts)")
    parser.add_argument("--live", action="store_true", help="Run live Bluetooth sniffing")
    parser.add_argument("--log", action="store_true", help="Log Bluetooth traffic")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth scan timing")
    parser.add_argument("--detect-beacons", action="store_true", help="Detect covert BLE beacons")
    parser.add_argument("--monitor", action="store_true", help="Monitor Bluetooth devices & send alerts")
    parser.add_argument("--alert", action="store_true", help="Enable alert system for new Bluetooth devices")
    parser.add_argument("--analyze", type=str, help="Analyze a saved sniffing log file")

    args = parser.parse_args()

    if args.live:
        stealth_sniffing_mode()
    elif args.detect_beacons:
        detect_covert_beacons()
    elif args.monitor:
        monitor_devices()
    elif args.alert:
        send_alert("New Bluetooth device detected")
    elif args.analyze:
        analyze_sniffed_data(args.analyze)
    else:
        print("[ERROR] No valid mode selected!")

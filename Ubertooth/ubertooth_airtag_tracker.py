import argparse
import subprocess
import time
import json
import os
import random
import csv

"""
Ubertooth AirTag Tracker

Features:
    - Detects & tracks hidden BLE AirTags & smart trackers used for stalking.
    - Scans for known Apple AirTags, Tile Trackers, and other BLE tracking devices.
    - Logs detected trackers and their movement over time.
    - Alerts if a tracker is following the user for extended periods.
    - Exports tracking data for further analysis (CSV/JSON).
    - Supports Covert Mode for stealth scanning.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: Python modules `json` and `csv` for logging.

Usage:
    - Scan for nearby BLE tracking devices (AirTags, Tile, etc.):
      python ubertooth_airtag_tracker.py --scan
    - Log detected AirTags & BLE trackers in real-time:
      python ubertooth_airtag_tracker.py --log airtag_log.json
    - Monitor AirTag movement & alert if it stays nearby too long:
      python ubertooth_airtag_tracker.py --monitor
    - Export tracking data for further analysis (CSV or JSON format):
      python ubertooth_airtag_tracker.py --export airtag_data.csv
    - Enable covert mode (stealth scanning to avoid alerting the AirTag):
      python ubertooth_airtag_tracker.py --scan --covert
"""

LOG_FILE = "airtag_log.json"
ALERT_THRESHOLD = 5  # Minutes before an alert triggers for suspicious tracking

TRACKER_SIGNATURES = {
    "airtag": "Apple Inc.",
    "tile": "Tile Inc.",
    "chipolo": "Chipolo",
    "smarttag": "Samsung SmartTag",
}

def log_event(event_data):
    """Logs detected AirTags and BLE trackers."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log AirTag tracking event: {e}")

def scan_airtags(covert=False):
    """Scans for AirTags & BLE tracking devices."""
    print("[INFO] Scanning for BLE tracking devices (AirTags, Tile, SmartTags)...")

    try:
        if covert:
            delay = random.uniform(2.0, 5.0)
            print(f"[COVERT MODE] Delaying scan by {delay:.2f} seconds...")
            time.sleep(delay)

        output = subprocess.check_output(["ubertooth-btle", "--scan-trackers"])
        devices = output.decode("utf-8").split("\n")

        detected_trackers = []
        for line in devices:
            for tracker, signature in TRACKER_SIGNATURES.items():
                if signature in line:
                    detected_trackers.append(line.strip())
                    print(f"[DETECTED] {tracker.upper()}: {line.strip()}")
                    log_event({"timestamp": time.time(), "device": line.strip(), "type": tracker.upper()})

        return detected_trackers

    except Exception as e:
        print(f"[ERROR] Failed to scan for AirTags: {e}")
        return []

def monitor_airtags():
    """Monitors AirTag presence and alerts if tracking is detected."""
    print("[INFO] Monitoring BLE tracking devices in real-time...")

    tracked_devices = {}
    
    try:
        while True:
            devices = scan_airtags()
            
            for device in devices:
                mac_address = device.split(" ")[1]  # Extract MAC address
                if mac_address in tracked_devices:
                    tracked_devices[mac_address]["last_seen"] = time.time()
                    tracked_devices[mac_address]["count"] += 1
                else:
                    tracked_devices[mac_address] = {"first_seen": time.time(), "last_seen": time.time(), "count": 1}
            
            for mac_address, data in tracked_devices.items():
                duration = (time.time() - data["first_seen"]) / 60  # Convert to minutes
                if duration > ALERT_THRESHOLD:
                    print(f"[ALERT] Suspicious tracker detected! MAC: {mac_address}, Duration: {duration:.2f} min")
                    log_event({"timestamp": time.time(), "device": mac_address, "alert": "Potential stalking detected", "duration": duration})

            time.sleep(10)

    except KeyboardInterrupt:
        print("[INFO] Stopping AirTag monitoring.")

def export_data(file_name):
    """Exports detected tracker data to a CSV file."""
    print(f"[INFO] Exporting detected AirTag data to {file_name}...")

    try:
        if file_name.endswith(".json"):
            os.rename(LOG_FILE, file_name)
        elif file_name.endswith(".csv"):
            with open(LOG_FILE, "r") as json_file:
                data = json.load(json_file)
            with open(file_name, "w", newline="") as csv_file:
                fieldnames = ["timestamp", "device", "type"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for entry in data:
                    writer.writerow({"timestamp": entry["timestamp"], "device": entry["device"], "type": entry["type"]})
        
        print("[SUCCESS] Export complete.")

    except Exception as e:
        print(f"[ERROR] Failed to export AirTag tracking data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth AirTag Tracker - Detect & Monitor BLE Trackers")
    parser.add_argument("--scan", action="store_true", help="Scan for hidden AirTags and BLE trackers")
    parser.add_argument("--monitor", action="store_true", help="Monitor BLE tracking devices in real-time")
    parser.add_argument("--covert", action="store_true", help="Enable stealth scanning to avoid detection")
    parser.add_argument("--export", type=str, help="Export detected tracker data (CSV/JSON format)")
    parser.add_argument("--log", type=str, help="Log detected trackers for forensic tracking")

    args = parser.parse_args()

    if args.scan:
        scan_airtags(covert=args.covert)
    elif args.monitor:
        monitor_airtags()
    elif args.export:
        export_data(args.export)
    else:
        print("[ERROR] No valid mode selected!")

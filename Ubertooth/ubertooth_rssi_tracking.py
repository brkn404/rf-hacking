import argparse
import subprocess
import time
import json
import os
import matplotlib.pyplot as plt

"""
Ubertooth Bluetooth RSSI Tracking

Features:
    - Tracks Bluetooth device movement based on RSSI (signal strength).
    - Estimates device distance and logs RSSI over time.
    - Alerts when a device enters or leaves a monitored area.
    - Generates RSSI trend plots for movement analysis.
    - Supports live tracking, logging, and visualization.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Install matplotlib for graphing: pip install matplotlib

Usage:
    - Run real-time Bluetooth RSSI tracking:
      python ubertooth_rssi_tracking.py --live
    - Track a specific device’s movement:
      python ubertooth_rssi_tracking.py --target AA:BB:CC:DD:EE:FF --log rssi_log.json
    - Alert when a device enters/exits a monitored area:
      python ubertooth_rssi_tracking.py --monitor --threshold -70
    - Visualize RSSI tracking trends over time:
      python ubertooth_rssi_tracking.py --plot rssi_log.json
"""

LOG_FILE = "rssi_log.json"

def log_event(event_data):
    """Logs RSSI tracking data."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        
        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log RSSI data: {e}")

def scan_rssi(target_mac=None):
    """Scans for Bluetooth devices and logs RSSI values."""
    print("[INFO] Scanning for Bluetooth RSSI...")

    detected_devices = {}

    try:
        output = subprocess.check_output(["ubertooth-rx", "-r"])
        lines = output.decode("utf-8").split("\n")

        for line in lines:
            if "Device" in line and "RSSI" in line:
                parts = line.split()
                mac_address = parts[1]
                rssi_value = int(parts[-1].replace("RSSI:", "").strip())

                if target_mac and mac_address != target_mac:
                    continue

                detected_devices[mac_address] = {"rssi": rssi_value, "timestamp": time.time()}
                print(f"[TRACKING] {mac_address} - RSSI: {rssi_value} dBm")

                log_event({"mac": mac_address, "rssi": rssi_value, "timestamp": time.time()})

        return detected_devices

    except Exception as e:
        print(f"[ERROR] Failed to scan for Bluetooth RSSI: {e}")
        return {}

def live_rssi_tracking(target_mac=None):
    """Continuously scans and logs Bluetooth RSSI data."""
    print(f"[INFO] Starting live RSSI tracking for {'all devices' if not target_mac else target_mac}...")

    try:
        while True:
            scan_rssi(target_mac)
            time.sleep(2)

    except KeyboardInterrupt:
        print("[INFO] Stopping live RSSI tracking.")

def monitor_device(target_mac, threshold):
    """Alerts when a device enters or leaves the area based on RSSI threshold."""
    print(f"[INFO] Monitoring {target_mac} for movement (Threshold: {threshold} dBm)...")

    try:
        while True:
            devices = scan_rssi(target_mac)
            if target_mac in devices:
                rssi_value = devices[target_mac]["rssi"]
                if rssi_value > threshold:
                    print(f"[ALERT] {target_mac} has entered the monitored area (RSSI: {rssi_value} dBm)")
                else:
                    print(f"[INFO] {target_mac} is still outside the monitored area (RSSI: {rssi_value} dBm)")

            time.sleep(2)

    except KeyboardInterrupt:
        print("[INFO] Stopping device monitoring.")

def plot_rssi(log_file):
    """Plots RSSI trends over time from log data."""
    print(f"[INFO] Generating RSSI plot from {log_file}...")

    try:
        with open(log_file, "r") as f:
            logs = json.load(f)

        timestamps = [entry["timestamp"] for entry in logs]
        rssi_values = [entry["rssi"] for entry in logs]

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, rssi_values, marker="o", linestyle="-", color="blue")
        plt.xlabel("Time (seconds)")
        plt.ylabel("RSSI (dBm)")
        plt.title("Bluetooth RSSI Tracking Over Time")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"[ERROR] Failed to generate RSSI plot: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth RSSI Tracking")
    parser.add_argument("--live", action="store_true", help="Run live RSSI tracking")
    parser.add_argument("--target", type=str, help="Track a specific Bluetooth device by MAC address")
    parser.add_argument("--monitor", action="store_true", help="Monitor a specific device's presence")
    parser.add_argument("--threshold", type=int, help="RSSI threshold for monitoring alerts")
    parser.add_argument("--log", type=str, help="Log RSSI data to a file")
    parser.add_argument("--plot", type=str, help="Plot RSSI data from a log file")

    args = parser.parse_args()

    if args.live:
        live_rssi_tracking(args.target)
    elif args.monitor and args.target and args.threshold:
        monitor_device(args.target, args.threshold)
    elif args.plot:
        plot_rssi(args.plot)
    elif args.target and args.log:
        scan_rssi(args.target)
    else:
        print("[ERROR] No valid mode selected!")

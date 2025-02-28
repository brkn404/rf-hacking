import argparse
import time
import subprocess
import json
import matplotlib.pyplot as plt
from collections import defaultdict

# -------------------------------------------
# Long-Range Bluetooth Tracking & Profiling
# -------------------------------------------
# Features:
# - Use Coded PHY on nRF52840 for long-range BLE scanning
# - Track RSSI values to determine movement patterns
# - Map device movements in real-time
# - Supports AirTags & Bluetooth beacons
#
# Requirements:
# - nRF52840 Dongle with Coded PHY support
# - Python 3.x
# - Nordic nRF Connect SDK (for Coded PHY support)
# - matplotlib for real-time mapping
#
# Usage:
# 1. Start long-range scanning:
#    python long_range_bluetooth_tracker.py --scan
# 2. Track a specific device:
#    python long_range_bluetooth_tracker.py --track XX:XX:XX:XX:XX:XX
# 3. Map device movements in real-time:
#    python long_range_bluetooth_tracker.py --map XX:XX:XX:XX:XX:XX
# -------------------------------------------

# Global variables to store tracking data
device_rssi_history = defaultdict(list)
device_positions = defaultdict(list)

def start_long_range_scan(duration=60):
    """
    Start long-range Bluetooth scanning using Coded PHY.
    """
    print(f"[+] Starting long-range Bluetooth scan for {duration} seconds...")
    try:
        # Use nRF Connect SDK or similar tool for Coded PHY scanning
        command = f"nrfutil scanner --coded-phy --duration {duration} --output scan_results.json"
        subprocess.run(command, shell=True, check=True)
        print("[✔] Scan complete. Results saved to scan_results.json")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during scan: {e}")

def track_device(mac_address):
    """
    Track a specific device by its MAC address and log RSSI values.
    """
    print(f"[+] Tracking device {mac_address}...")
    try:
        # Continuously monitor RSSI values for the target device
        while True:
            command = f"nrfutil scanner --coded-phy --filter {mac_address} --rssi"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            rssi = int(result.stdout.strip().split(":")[-1])
            device_rssi_history[mac_address].append((time.time(), rssi))
            print(f"[*] Device {mac_address} - RSSI: {rssi} dBm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("[✔] Tracking stopped.")
    except Exception as e:
        print(f"[!] Error during tracking: {e}")

def map_device_movements(mac_address):
    """
    Map the movement of a device based on RSSI values.
    """
    print(f"[+] Mapping movements for device {mac_address}...")
    try:
        # Load RSSI history for the device
        if mac_address not in device_rssi_history:
            print(f"[!] No RSSI data found for device {mac_address}. Start tracking first.")
            return

        timestamps, rssi_values = zip(*device_rssi_history[mac_address])

        # Plot RSSI values over time
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, rssi_values, label=f"Device {mac_address}")
        plt.xlabel("Time (s)")
        plt.ylabel("RSSI (dBm)")
        plt.title(f"Device {mac_address} Movement Tracking")
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"[!] Error during mapping: {e}")

def main():
    parser = argparse.ArgumentParser(description="Long-Range Bluetooth Tracking & Profiling")
    parser.add_argument("--scan", action='store_true', help="Start long-range Bluetooth scanning")
    parser.add_argument("--track", type=str, help="Track a specific device by MAC address")
    parser.add_argument("--map", type=str, help="Map movements of a specific device by MAC address")
    parser.add_argument("--duration", type=int, default=60, help="Duration of the scan in seconds")
    args = parser.parse_args()

    if args.scan:
        start_long_range_scan(args.duration)
    elif args.track:
        track_device(args.track)
    elif args.map:
        map_device_movements(args.map)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
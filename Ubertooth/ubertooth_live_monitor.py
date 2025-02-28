import argparse
import subprocess
import json
import os
import time
import curses

"""
Ubertooth Bluetooth Live Monitor

Features:
    - Monitors active Bluetooth Classic (BR/EDR) and BLE devices in real-time.
    - Displays device MAC address, signal strength (RSSI), and device type.
    - Allows filtering by device type (e.g., audio, keyboard, mouse).
    - Tracks a specific Bluetooth MAC address over time.
    - Logs detected devices for forensic analysis.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Run live Bluetooth traffic monitoring and log detected devices:
      python ubertooth_live_monitor.py --log bt_live_devices.json
    - Filter monitoring by device type (e.g., `audio`, `keyboard`, `mouse`):
      python ubertooth_live_monitor.py --filter audio
    - Track a specific Bluetooth MAC address in real-time:
      python ubertooth_live_monitor.py --track AA:BB:CC:DD:EE:FF
    - Monitor Bluetooth traffic with RSSI signal strength tracking:
      python ubertooth_live_monitor.py --rssi
    - Display a real-time dashboard with active Bluetooth devices:
      python ubertooth_live_monitor.py --dashboard
"""

LOG_FILE = "bt_live_devices.json"

def scan_bluetooth_live(filter_type=None, track_mac=None, log_file=None, display_dashboard=False, rssi=False):
    """Monitors Bluetooth devices in real-time and logs detected activity."""
    
    detected_devices = {}
    
    def update_display(stdscr):
        stdscr.nodelay(1)
        curses.curs_set(0)

        while True:
            try:
                output = subprocess.check_output(["ubertooth-rx", "-s"])
                lines = output.decode("utf-8").split("\n")

                for line in lines:
                    if "Device" in line:
                        parts = line.split()
                        if len(parts) > 2:
                            mac_address = parts[1]
                            device_type = "BLE" if "BLE" in line else "Classic"
                            rssi_value = parts[-1] if rssi else "N/A"

                            # Apply filtering if specified
                            if filter_type and filter_type.lower() not in line.lower():
                                continue

                            # Track a specific MAC if provided
                            if track_mac and track_mac.lower() != mac_address.lower():
                                continue

                            detected_devices[mac_address] = {"device_type": device_type, "rssi": rssi_value, "last_seen": time.time()}
                            stdscr.clear()
                            stdscr.addstr(0, 0, "Ubertooth Bluetooth Live Monitor", curses.A_BOLD)
                            stdscr.addstr(1, 0, "-------------------------------------------------")
                            row = 2
                            for mac, info in detected_devices.items():
                                stdscr.addstr(row, 0, f"[{info['device_type']}] {mac}  RSSI: {info['rssi']} dBm")
                                row += 1
                            stdscr.refresh()

                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(detected_devices, f, indent=4)

                time.sleep(2)

            except KeyboardInterrupt:
                stdscr.addstr(row + 2, 0, "[INFO] Stopping Bluetooth live monitoring...")
                stdscr.refresh()
                time.sleep(2)
                break
            except Exception as e:
                stdscr.addstr(row + 2, 0, f"[ERROR] {str(e)}")
                stdscr.refresh()
                time.sleep(2)
    
    if display_dashboard:
        curses.wrapper(update_display)
    else:
        while True:
            try:
                output = subprocess.check_output(["ubertooth-rx", "-s"])
                lines = output.decode("utf-8").split("\n")

                for line in lines:
                    if "Device" in line:
                        parts = line.split()
                        if len(parts) > 2:
                            mac_address = parts[1]
                            device_type = "BLE" if "BLE" in line else "Classic"
                            rssi_value = parts[-1] if rssi else "N/A"

                            if filter_type and filter_type.lower() not in line.lower():
                                continue
                            if track_mac and track_mac.lower() != mac_address.lower():
                                continue

                            detected_devices[mac_address] = {"device_type": device_type, "rssi": rssi_value, "last_seen": time.time()}
                            print(f"[{device_type}] {mac_address}  RSSI: {rssi_value} dBm")

                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(detected_devices, f, indent=4)

                time.sleep(2)

            except KeyboardInterrupt:
                print("[INFO] Stopping Bluetooth live monitoring...")
                break
            except Exception as e:
                print(f"[ERROR] {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Live Monitor")
    parser.add_argument("--log", type=str, help="Log file to save detected devices")
    parser.add_argument("--filter", type=str, help="Filter devices by type (e.g., audio, keyboard, mouse)")
    parser.add_argument("--track", type=str, help="Track a specific Bluetooth MAC address")
    parser.add_argument("--rssi", action="store_true", help="Enable RSSI signal strength tracking")
    parser.add_argument("--dashboard", action="store_true", help="Display real-time Bluetooth traffic in a curses-based dashboard")

    args = parser.parse_args()

    scan_bluetooth_live(filter_type=args.filter, track_mac=args.track, log_file=args.log, display_dashboard=args.dashboard, rssi=args.rssi)

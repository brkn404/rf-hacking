import asyncio
from bleak import BleakScanner
import datetime
import argparse
import json

"""
Real-Time BLE Device Tracking (Beacon Monitoring)

Features:
    - Continuously scans for a specific BLE device based on MAC address.
    - Logs signal strength (RSSI) to estimate proximity over time.
    - Sends alerts when a device enters or exits a given area.
    - Outputs results to a JSON log for tracking proximity history.

Requirements:
    - Adafruit Bluefruit LE Sniffer with nRF Sniffer firmware
    - Python libraries: bleak

Run Commands:
    - Track a BLE device in real-time:
      python ble_device_tracker.py --target <MAC_ADDRESS> --log ble_tracking_log.json --threshold -70
"""

async def track_device(target_mac, log_file, threshold):
    """Continuously scans for a specific BLE device and logs its RSSI."""
    print(f"[INFO] Tracking BLE device: {target_mac}")
    device_detected = False
    
    try:
        while True:
            devices = await BleakScanner.discover()
            for device in devices:
                if device.address.lower() == target_mac.lower():
                    rssi = device.rssi
                    timestamp = datetime.datetime.now().isoformat()
                    log_entry = {"timestamp": timestamp, "rssi": rssi, "device": target_mac}
                    
                    with open(log_file, "a") as f:
                        json.dump(log_entry, f)
                        f.write("\n")
                    
                    print(f"[DETECTED] {target_mac} RSSI: {rssi}")
                    
                    if rssi > threshold and not device_detected:
                        print(f"[ALERT] {target_mac} has entered the monitored area!")
                        device_detected = True
                    elif rssi <= threshold and device_detected:
                        print(f"[ALERT] {target_mac} has exited the monitored area!")
                        device_detected = False
    
    except KeyboardInterrupt:
        print("[INFO] Stopping BLE tracking.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-Time BLE Device Tracking")
    parser.add_argument("--target", required=True, help="MAC address of the BLE device to track")
    parser.add_argument("--log", default="ble_tracking_log.json", help="File to log detected BLE device RSSI")
    parser.add_argument("--threshold", type=int, default=-70, help="RSSI threshold for entry/exit alerts")
    args = parser.parse_args()
    
    asyncio.run(track_device(args.target, args.log, args.threshold))

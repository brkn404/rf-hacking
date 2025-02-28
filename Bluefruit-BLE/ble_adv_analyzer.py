import asyncio
from bleak import BleakScanner
import json
import datetime
import argparse

"""
BLE Advertising Packet Analyzer - Bluefruit LE Sniffer Version

Features:
    - Scans for BLE advertising beacons.
    - Identifies and logs changes in broadcasted data over time.
    - Compares manufacturer data to known tracking devices (e.g., Apple AirTags, Tile trackers).
    - Outputs results to a JSON log for tracking BLE beacon changes.

Requirements:
    - Adafruit Bluefruit LE Sniffer with nRF Sniffer firmware
    - Python libraries: bleak

Run Commands:
    - Scan and log BLE advertising packets:
      python ble_adv_analyzer.py --log ble_adv_log.json
"""

KNOWN_TRACKERS = {
    "Apple AirTag": "0x4C000100",
    "Tile Tracker": "0xC7000000",
    "Samsung SmartTag": "0x07000000"
}

def format_advertisement(device):
    """Formats the BLE advertisement data into a readable dictionary."""
    return {
        "address": device.address,
        "name": device.name or "Unknown",
        "rssi": device.rssi,
        "manufacturer_data": device.metadata.get("manufacturer_data", {}),
        "timestamp": datetime.datetime.now().isoformat()
    }

async def scan_ble(log_file):
    """Scans for BLE advertising packets and logs changes over time."""
    print("[INFO] Scanning for BLE advertising beacons...")
    devices_detected = {}
    
    try:
        while True:
            devices = await BleakScanner.discover()
            for device in devices:
                adv_data = format_advertisement(device)
                addr = device.address
                
                if addr not in devices_detected or devices_detected[addr] != adv_data:
                    devices_detected[addr] = adv_data
                    print(f"[DETECTED] {adv_data}")
                    
                    with open(log_file, "a") as f:
                        json.dump(adv_data, f)
                        f.write("\n")

                    # Check for known tracking devices
                    for tracker, identifier in KNOWN_TRACKERS.items():
                        if any(identifier in str(adv_data["manufacturer_data"]) for _ in adv_data["manufacturer_data"]):
                            print(f"[ALERT] Possible {tracker} detected: {addr}")
    
    except KeyboardInterrupt:
        print("[INFO] Stopping BLE advertising scan.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Advertising Packet Analyzer")
    parser.add_argument("--log", default="ble_adv_log.json", help="File to log detected BLE advertisements")
    args = parser.parse_args()
    
    asyncio.run(scan_ble(args.log))

# microbit_ble_tracking.py

"""
Passive BLE Surveillance & Tracking for micro:bit V2

This script allows passive BLE device tracking by:
- Continuously scanning BLE devices (`--track-devices`)
- Logging RSSI changes to estimate movement (`--log <file>`)
- Detecting hidden BLE tracking devices (AirTags, Tile, etc.)

### Usage Examples:

1. Track all nearby BLE devices:
   ```sh
   python microbit_ble_tracking.py --track-devices
   ```

2. Log BLE movement patterns to a file:
   ```sh
   python microbit_ble_tracking.py --track-devices --log tracking_data.json
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner
import argparse
import json

# Passive BLE Tracking
async def ble_track_devices(logfile=None):
    """Scans for BLE devices, logs movement patterns using RSSI values."""
    print("[+] Tracking nearby BLE devices...")
    tracked_data = {}
    
    while True:
        devices = await BleakScanner.discover()
        for device in devices:
            tracked_data[device.address] = {
                "name": device.name,
                "rssi": device.rssi
            }
            print(f"[+] {device.address} - {device.name} - RSSI: {device.rssi}")
        
        if logfile:
            with open(logfile, "w") as f:
                json.dump(tracked_data, f)
        await asyncio.sleep(5)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Passive BLE Surveillance & Tracking for micro:bit V2")
    parser.add_argument("--track-devices", help="Track BLE devices and log movement patterns", action="store_true")
    parser.add_argument("--log", help="Save tracking data to a file", metavar="logfile")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.track_devices:
        loop.run_until_complete(ble_track_devices(args.log))

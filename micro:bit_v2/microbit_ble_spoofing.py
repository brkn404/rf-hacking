# microbit_ble_spoofing.py

"""
BLE Beacon Spoofing & Cloning for micro:bit V2

This script allows BLE beacon spoofing and cloning by:
- Broadcasting fake BLE advertisements (`--spoof <name> <uuid> <major> <minor>`)
- Cloning an existing BLE beacon (`--clone <target_mac>`)

### Usage Examples:

1. Spoof a BLE beacon with a custom name, UUID, and values:
   ```sh
   python microbit_ble_spoofing.py --spoof FakeBeacon 12345678-1234-5678-1234-567812345678 100 200
   ```

2. Clone an existing BLE beacon:
   ```sh
   python microbit_ble_spoofing.py --clone AA:BB:CC:DD:EE:FF
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner, BleakClient, BleakAdvertiser
import argparse

# Spoof a BLE Beacon
async def ble_spoof_beacon(name, uuid, major, minor):
    """Broadcasts a fake BLE beacon with custom values."""
    print(f"[+] Spoofing BLE Beacon: {name} - UUID: {uuid}, Major: {major}, Minor: {minor}")
    advertiser = BleakAdvertiser()
    await advertiser.start(name=name, manufacturer_data={0x004C: [int(major), int(minor)]})
    await asyncio.sleep(30)  # Advertise for 30 seconds
    await advertiser.stop()
    print("[+] Spoofing complete.")

# Clone an Existing BLE Beacon
async def ble_clone_beacon(target_mac):
    """Clones an existing BLE beacon's advertisement data."""
    print(f"[+] Cloning BLE Beacon from {target_mac}...")
    devices = await BleakScanner.discover()
    for device in devices:
        if device.address == target_mac:
            print(f"[+] Found {target_mac}: Cloning beacon data...")
            advertiser = BleakAdvertiser()
            await advertiser.start(name=device.name, manufacturer_data=device.metadata.get("manufacturer_data", {}))
            await asyncio.sleep(30)  # Advertise for 30 seconds
            await advertiser.stop()
            print("[+] Cloning complete.")
            return
    print("[-] Target beacon not found.")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Beacon Spoofing & Cloning for micro:bit V2")
    parser.add_argument("--spoof", nargs=4, metavar=("name", "uuid", "major", "minor"), help="Spoof a BLE beacon with given values")
    parser.add_argument("--clone", help="Clone an existing BLE beacon", metavar="target_mac")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.spoof:
        loop.run_until_complete(ble_spoof_beacon(*args.spoof))
    elif args.clone:
        loop.run_until_complete(ble_clone_beacon(args.clone))

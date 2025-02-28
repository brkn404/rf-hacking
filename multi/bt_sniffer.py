import argparse
import os
import time
from scapy.all import *

# -------------------------------------------
# Bluetooth Sniffer - BLE & Classic
# -------------------------------------------
# Features:
# - Captures both BLE & Classic Bluetooth packets
# - Logs all detected Bluetooth devices
# - Supports active & passive scanning
# - Detects unpaired devices & insecure connections
# - Live packet analysis for real-time monitoring
# - Bluetooth fingerprinting to identify device types
# - Supports decryption of captured packets (if keys available)
# - Automated Bluetooth profiling for device behavior analysis
# - Adaptive attack strategies based on detected devices
#
# Requirements:
# - Nordic nRF52840 Dongle / Adafruit Bluefruit LE Sniffer
# - Ubertooth One (for Classic BT sniffing)
# - Python 3.x
# - Scapy (for packet parsing)
#
# Usage:
# 1. Scan for all Bluetooth devices:
#    python bt_sniffer.py --scan
# 2. Log discovered devices to a file:
#    python bt_sniffer.py --scan --log
# 3. Capture BLE packets in real-time:
#    python bt_sniffer.py --ble
# 4. Capture Classic Bluetooth packets:
#    python bt_sniffer.py --classic
# 5. Enable live packet analysis:
#    python bt_sniffer.py --live
# 6. Perform Bluetooth fingerprinting:
#    python bt_sniffer.py --fingerprint
# 7. Attempt decryption of captured packets:
#    python bt_sniffer.py --decrypt --keyfile keys.txt
# 8. Run automated Bluetooth profiling:
#    python bt_sniffer.py --profile
# 9. Apply adaptive attack strategies based on detected devices:
#    python bt_sniffer.py --adaptive-attack
# -------------------------------------------

def scan_bluetooth(log=False):
    """Scans for nearby Bluetooth devices."""
    print("[+] Scanning for Bluetooth devices...")
    os.system("hcitool scan > bt_scan_results.txt")
    os.system("hcitool lescan --passive > ble_scan_results.txt & sleep 10; pkill --signal SIGINT hcitool")
    
    if log:
        print("[✔] Scan results saved to bt_scan_results.txt & ble_scan_results.txt")
    else:
        print("[✔] Scan complete. Run with --log to save results.")

def capture_ble():
    """Captures BLE packets using the nRF52840 dongle."""
    print("[+] Capturing BLE packets...")
    os.system("btlejack -i 0 -f 37,38,39 -c")
    print("[✔] BLE capture complete.")

def capture_classic():
    """Captures Classic Bluetooth packets using Ubertooth One."""
    print("[+] Capturing Classic Bluetooth packets...")
    os.system("ubertooth-bt -f -c bt_classic_capture.pcap")
    print("[✔] Classic Bluetooth capture saved to bt_classic_capture.pcap")

def live_analysis():
    """Analyzes Bluetooth packets live."""
    print("[+] Starting live packet analysis...")
    os.system("tshark -i bluetooth0 -Y 'btcommon' -V")

def fingerprint_devices():
    """Attempts to identify Bluetooth device types based on packet data."""
    print("[+] Performing Bluetooth fingerprinting...")
    os.system("python bt_fingerprint.py --input bt_scan_results.txt")

def decrypt_packets(keyfile):
    """Attempts to decrypt captured Bluetooth packets using provided keys."""
    print(f"[+] Attempting decryption using keyfile {keyfile}...")
    os.system(f"btlejack -i 0 --decrypt -k {keyfile}")

def profile_bluetooth_behavior():
    """Analyzes Bluetooth device behavior based on packet patterns."""
    print("[+] Running Bluetooth device profiling...")
    os.system("python bt_behavior_analysis.py --input bt_scan_results.txt")

def adaptive_attack():
    """Applies attack strategies based on detected device types and vulnerabilities."""
    print("[+] Analyzing Bluetooth devices for adaptive attack strategies...")
    os.system("python bt_adaptive_attack.py --input bt_scan_results.txt")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Sniffer - BLE & Classic")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth devices")
    parser.add_argument("--log", action='store_true', help="Log discovered devices")
    parser.add_argument("--ble", action='store_true', help="Capture BLE packets")
    parser.add_argument("--classic", action='store_true', help="Capture Classic Bluetooth packets")
    parser.add_argument("--live", action='store_true', help="Enable live packet analysis")
    parser.add_argument("--fingerprint", action='store_true', help="Perform Bluetooth fingerprinting")
    parser.add_argument("--decrypt", type=str, help="Attempt decryption of captured packets using keyfile")
    parser.add_argument("--profile", action='store_true', help="Run automated Bluetooth profiling")
    parser.add_argument("--adaptive-attack", action='store_true', help="Apply adaptive attack strategies based on detected devices")
    args = parser.parse_args()

    if args.scan:
        scan_bluetooth(args.log)
    elif args.ble:
        capture_ble()
    elif args.classic:
        capture_classic()
    elif args.live:
        live_analysis()
    elif args.fingerprint:
        fingerprint_devices()
    elif args.decrypt:
        decrypt_packets(args.decrypt)
    elif args.profile:
        profile_bluetooth_behavior()
    elif args.adaptive_attack:
        adaptive_attack()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

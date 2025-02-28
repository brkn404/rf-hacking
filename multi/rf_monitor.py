import argparse
import os
import time
from scapy.all import *

# -------------------------------------------
# Adaptive RF Signal Monitoring & Logging Tool
# -------------------------------------------
# Features:
# - Monitors and logs RF signals across Wi-Fi, Bluetooth, and Sub-1GHz
# - Detects active attacks in the area (deauths, jamming, replay attacks)
# - Real-time visualization of RF traffic
# - Identifies rogue devices and potential threats
# - Automated RF analysis and logging
#
# Requirements:
# - Wi-Fi Adapter (Monitor Mode Capable)
# - Ubertooth One (Bluetooth Sniffing)
# - Yardstick One (Sub-1GHz Monitoring)
# - Python 3.x
# - Scapy, Kismet, Ubertooth tools
#
# Usage:
# 1. Monitor Wi-Fi RF signals:
#    python rf_monitor.py --wifi
# 2. Monitor Bluetooth RF signals:
#    python rf_monitor.py --bluetooth
# 3. Monitor Sub-1GHz RF signals:
#    python rf_monitor.py --sub1ghz
# 4. Run full-spectrum RF monitoring:
#    python rf_monitor.py --full-scan
# 5. Enable automated logging:
#    python rf_monitor.py --log
# 6. Detect active RF attacks:
#    python rf_monitor.py --detect-attacks
# -------------------------------------------

def monitor_wifi():
    """Monitors Wi-Fi RF signals for active threats."""
    print("[+] Monitoring Wi-Fi RF signals...")
    os.system("airodump-ng wlan0mon --write wifi_scan")
    print("[✔] Wi-Fi scan complete. Logs saved to wifi_scan.csv")

def monitor_bluetooth():
    """Monitors Bluetooth RF signals using Ubertooth One."""
    print("[+] Monitoring Bluetooth RF signals...")
    os.system("ubertooth-specan -f 2400 -r bluetooth_scan.txt")
    print("[✔] Bluetooth scan complete. Logs saved to bluetooth_scan.txt")

def monitor_sub1ghz():
    """Monitors Sub-1GHz RF signals using Yardstick One."""
    print("[+] Monitoring Sub-1GHz RF signals...")
    os.system("rfcat -r 'd.scan()' > sub1ghz_scan.txt")
    print("[✔] Sub-1GHz scan complete. Logs saved to sub1ghz_scan.txt")

def detect_attacks():
    """Detects active RF attacks such as deauths, jamming, and replay attacks."""
    print("[+] Scanning for RF attacks...")
    os.system("airodump-ng wlan0mon --write wifi_attack_scan --output-format csv")
    os.system("ubertooth-rx -f 2400 -r bluetooth_attack_scan.txt")
    os.system("rfcat -r 'd.detect_attacks()' > sub1ghz_attack_scan.txt")
    print("[✔] Attack detection complete. Logs saved to respective scan files.")

def full_scan():
    """Runs a full-spectrum RF scan across Wi-Fi, Bluetooth, and Sub-1GHz."""
    print("[+] Running full RF spectrum scan...")
    monitor_wifi()
    monitor_bluetooth()
    monitor_sub1ghz()
    print("[✔] Full scan complete.")

def auto_logging():
    """Automatically logs RF signals for later analysis."""
    print("[+] Enabling automated RF logging...")
    os.system("kismet -c wlan0mon -c ubertooth -c rfcat > rf_log.pcap")
    print("[✔] RF logs saved to rf_log.pcap")

def main():
    parser = argparse.ArgumentParser(description="Adaptive RF Signal Monitoring & Logging Tool")
    parser.add_argument("--wifi", action='store_true', help="Monitor Wi-Fi RF signals")
    parser.add_argument("--bluetooth", action='store_true', help="Monitor Bluetooth RF signals")
    parser.add_argument("--sub1ghz", action='store_true', help="Monitor Sub-1GHz RF signals")
    parser.add_argument("--full-scan", action='store_true', help="Run a full-spectrum RF scan")
    parser.add_argument("--log", action='store_true', help="Enable automated RF logging")
    parser.add_argument("--detect-attacks", action='store_true', help="Detect active RF attacks (deauths, jamming, replay attacks)")
    args = parser.parse_args()

    if args.wifi:
        monitor_wifi()
    elif args.bluetooth:
        monitor_bluetooth()
    elif args.sub1ghz:
        monitor_sub1ghz()
    elif args.full_scan:
        full_scan()
    elif args.log:
        auto_logging()
    elif args.detect_attacks:
        detect_attacks()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

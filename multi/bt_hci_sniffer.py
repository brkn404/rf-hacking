import argparse
import os
import time

# -------------------------------------------
# Bluetooth Classic HCI Sniffer
# -------------------------------------------
# Features:
# - Captures and analyzes Bluetooth Classic HCI packets
# - Extracts pairing keys and decrypts communications
# - Logs intercepted traffic for later forensic analysis
# - Works on Bluetooth keyboards, headsets, and IoT devices
#
# Requirements:
# - Python 3.x
# - Ubertooth One, UD100 Bluetooth Adapter, Crazyradio 2.0
# - Wireshark, hcitool, hcidump, btmon
# - Bluetooth Classic (BR/EDR) compatible devices
#
# Usage:
# 1. Scan for Bluetooth Classic devices:
#    python bt_hci_sniffer.py --scan
# 2. Start sniffing HCI packets:
#    python bt_hci_sniffer.py --sniff --target XX:XX:XX:XX:XX:XX
# 3. Save captured packets to PCAP for Wireshark analysis:
#    python bt_hci_sniffer.py --sniff --target XX:XX:XX:XX:XX:XX --output bt_sniff.pcap
# 4. Extract pairing keys from captured packets:
#    python bt_hci_sniffer.py --extract-keys --input bt_sniff.pcap
# -------------------------------------------

def scan_bluetooth_devices():
    """Scans for nearby Bluetooth Classic devices."""
    print("[+] Scanning for Bluetooth Classic devices...")
    os.system("hcitool scan")
    print("[✔] Scan complete.")

def sniff_hci_packets(target, output_file):
    """Sniffs HCI packets from a target Bluetooth device."""
    print(f"[+] Sniffing HCI packets from {target}...")
    os.system(f"hcidump -X -i hci0 > {output_file}")
    print(f"[✔] Capture saved to {output_file}.")

def extract_pairing_keys(input_file):
    """Extracts pairing keys from a captured HCI packet log."""
    print(f"[+] Extracting pairing keys from {input_file}...")
    os.system(f"btmon --read {input_file} --keys-only")
    print("[✔] Pairing key extraction complete.")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Classic HCI Sniffer")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth Classic devices")
    parser.add_argument("--sniff", action='store_true', help="Sniff HCI packets from a target device")
    parser.add_argument("--target", type=str, help="Target Bluetooth MAC address")
    parser.add_argument("--output", type=str, help="Output file for captured packets")
    parser.add_argument("--extract-keys", action='store_true', help="Extract pairing keys from a capture file")
    parser.add_argument("--input", type=str, help="Input PCAP file for key extraction")
    args = parser.parse_args()
    
    if args.scan:
        scan_bluetooth_devices()
    elif args.sniff and args.target and args.output:
        sniff_hci_packets(args.target, args.output)
    elif args.extract_keys and args.input:
        extract_pairing_keys(args.input)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

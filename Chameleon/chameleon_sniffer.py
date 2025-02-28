import argparse
import os
import time

# -------------------------------------------
# Chameleon Ultra - NFC Sniffer & Logger Tool
# -------------------------------------------
# Features:
# - Captures live NFC traffic for analysis
# - Logs raw NFC transactions for further review
# - Identifies common NFC communication patterns
# - Supports real-time packet inspection and decoding
# - Stealth mode for undetectable NFC sniffing
# - Real-time NFC relay integration for on-the-fly attacks
# - Automated protocol classification for identifying NFC communication types
# - Decrypts encrypted NFC traffic for advanced security analysis
# - Multi-device packet correlation for detecting suspicious activities
# - Works with Chameleon Ultra & integrates with Proxmark3
#
# Requirements:
# - Chameleon Ultra device
# - Python 3.x
# - LibNFC / Proxmark3 / Chameleon Ultra CLI tools
#
# Usage:
# 1. Start NFC traffic sniffing:
#    python chameleon_sniffer.py --sniff --output logs/nfc_traffic.log
# 2. Analyze captured NFC packets:
#    python chameleon_sniffer.py --analyze --input logs/nfc_traffic.log
# 3. Enable real-time monitoring:
#    python chameleon_sniffer.py --live-monitor
# 4. Enable stealth mode for covert NFC sniffing:
#    python chameleon_sniffer.py --stealth --sniff --output logs/nfc_traffic.log
# 5. Integrate real-time NFC relay into sniffing:
#    python chameleon_sniffer.py --relay-sniff --output logs/nfc_traffic.log
# 6. Perform automated protocol classification:
#    python chameleon_sniffer.py --classify --input logs/nfc_traffic.log
# 7. Decrypt encrypted NFC traffic:
#    python chameleon_sniffer.py --decrypt --input logs/nfc_traffic.log
# 8. Correlate NFC packets across multiple devices:
#    python chameleon_sniffer.py --correlate --device-list devices.txt
# -------------------------------------------

def start_sniffing(output_file, stealth=False, relay_sniff=False):
    """Captures live NFC traffic and logs it to a file, with optional stealth and relay integration."""
    print(f"[+] Starting NFC traffic sniffing, saving to {output_file}...")
    cmd = f"chamtool sniff --output {output_file}"
    
    if stealth:
        cmd += " --stealth"
    if relay_sniff:
        cmd += " --relay"
    
    os.system(cmd)
    print("[✔] NFC traffic logged successfully.")

def analyze_packets(input_file):
    """Analyzes captured NFC traffic for patterns and vulnerabilities."""
    print(f"[+] Analyzing NFC traffic from {input_file}...")
    os.system(f"chamtool analyze --input {input_file}")
    print("[✔] Analysis complete.")

def classify_protocols(input_file):
    """Automatically classifies detected NFC communication types."""
    print(f"[+] Performing protocol classification on {input_file}...")
    os.system(f"chamtool classify --input {input_file}")
    print("[✔] Protocol classification complete.")

def decrypt_nfc_traffic(input_file):
    """Decrypts encrypted NFC traffic for advanced security analysis."""
    print(f"[+] Attempting to decrypt NFC traffic from {input_file}...")
    os.system(f"chamtool decrypt --input {input_file}")
    print("[✔] NFC decryption complete.")

def correlate_packets(device_list):
    """Correlates NFC packet data across multiple devices."""
    print(f"[+] Correlating NFC packet data across devices in {device_list}...")
    os.system(f"chamtool correlate --devices {device_list}")
    print("[✔] Multi-device packet correlation complete.")

def live_monitor():
    """Enables real-time NFC monitoring and packet analysis."""
    print("[+] Starting live NFC monitoring...")
    os.system("chamtool monitor --live")
    print("[✔] Live monitoring active.")

def main():
    parser = argparse.ArgumentParser(description="Chameleon Ultra - NFC Sniffer & Logger Tool")
    parser.add_argument("--sniff", action='store_true', help="Capture live NFC traffic and log it")
    parser.add_argument("--analyze", action='store_true', help="Analyze captured NFC traffic logs")
    parser.add_argument("--live-monitor", action='store_true', help="Enable real-time NFC monitoring")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode for covert NFC sniffing")
    parser.add_argument("--relay-sniff", action='store_true', help="Integrate real-time NFC relay into sniffing")
    parser.add_argument("--classify", action='store_true', help="Perform automated protocol classification on captured traffic")
    parser.add_argument("--decrypt", action='store_true', help="Attempt to decrypt encrypted NFC traffic")
    parser.add_argument("--correlate", type=str, help="Correlate NFC packets across multiple devices using a device list")
    parser.add_argument("--output", type=str, help="Output file for logging captured NFC traffic")
    parser.add_argument("--input", type=str, help="Input file for analyzing NFC logs")
    parser.add_argument("--device-list", type=str, help="Specify a list of devices for packet correlation")
    args = parser.parse_args()

    if args.sniff and args.output:
        start_sniffing(args.output, args.stealth, args.relay_sniff)
    elif args.analyze and args.input:
        analyze_packets(args.input)
    elif args.classify and args.input:
        classify_protocols(args.input)
    elif args.decrypt and args.input:
        decrypt_nfc_traffic(args.input)
    elif args.correlate and args.device_list:
        correlate_packets(args.device_list)
    elif args.live_monitor:
        live_monitor()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

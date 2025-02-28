import argparse
import os
import time

# -------------------------------------------
# SDR Packet Capture & Analysis Tool
# -------------------------------------------
# Features:
# - Captures RF traffic from SDR devices and saves it in PCAP format
# - Supports Bluetooth, Wi-Fi, Zigbee, GSM, ADS-B, and custom RF protocols
# - Compatible with Wireshark for deep packet inspection
# - Automates frequency selection and protocol-based filtering
# - Logs raw signal captures for forensic analysis
#
# Requirements:
# - Python 3.x
# - SoapySDR, GNU Radio, gr-gsm, Wireshark, Kismet
# - Compatible SDR (LimeSDR, HackRF, RTL-SDR, or BladeRF)
#
# Usage:
# 1. Capture Bluetooth traffic:
#    python sdr_pcap_logger.py --capture --protocol bluetooth --output bt_traffic.pcap
# 2. Capture Wi-Fi traffic on 2.4GHz:
#    python sdr_pcap_logger.py --capture --protocol wifi --freq 2.4GHz --output wifi_traffic.pcap
# 3. Capture GSM network signals:
#    python sdr_pcap_logger.py --capture --protocol gsm --output gsm_traffic.pcap
# 4. Capture raw RF traffic for unknown protocols:
#    python sdr_pcap_logger.py --capture --freq 915MHz --output raw_rf_capture.pcap
# -------------------------------------------

def capture_rf_traffic(protocol, freq, output_file):
    """Captures RF traffic and logs it to a PCAP file."""
    print(f"[+] Capturing {protocol} traffic on {freq}...")
    os.system(f"python sdr_rf_sniffer.py --protocol {protocol} --freq {freq} --output {output_file}")
    print(f"[✔] Capture saved to {output_file}.")

def main():
    parser = argparse.ArgumentParser(description="SDR Packet Capture & Analysis Tool")
    parser.add_argument("--capture", action='store_true', help="Capture RF traffic and save as PCAP")
    parser.add_argument("--protocol", type=str, help="Target protocol (e.g., Bluetooth, Wi-Fi, GSM, Zigbee)")
    parser.add_argument("--freq", type=str, help="Target frequency (e.g., 2.4GHz, 915MHz, 5GHz)")
    parser.add_argument("--output", type=str, help="Output PCAP file")
    args = parser.parse_args()
    
    if args.capture and args.protocol and args.output:
        freq = args.freq if args.freq else "auto"
        capture_rf_traffic(args.protocol, freq, args.output)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

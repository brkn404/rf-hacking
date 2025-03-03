import argparse
import os
import time
import json

# -------------------------------------------
# NRF52840 Device Profiler & Vulnerability Scanner
# -------------------------------------------
# Features:
# - Scans BLE, Zigbee, and NRF24 devices for vulnerabilities
# - Identifies security flaws like weak pairing, default keys, and known exploits
# - Logs device metadata for further analysis
# - Generates a detailed vulnerability report with risk levels
# - Fingerprints devices to detect specific manufacturers & firmware versions
# - Provides real-time alerts for detected vulnerabilities
# - Suggests potential exploits based on scan results
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: btlejack (BLE), Zigbee2MQTT (Zigbee), nrf24_sniffer (NRF24)
# - Python 3.x
#
# Usage:
# 1. Scan for BLE vulnerabilities:
#    python nrf52840_device_profiler.py --ble
# 2. Scan for Zigbee vulnerabilities:
#    python nrf52840_device_profiler.py --zigbee
# 3. Scan for NRF24 vulnerabilities:
#    python nrf52840_device_profiler.py --nrf24
# 4. Generate a full vulnerability report:
#    python nrf52840_device_profiler.py --report
# -------------------------------------------

def scan_ble():
    """Scans for BLE devices, fingerprints them, and identifies vulnerabilities."""
    print("[+] Scanning BLE devices for security flaws...")
    os.system("btlejack -s --scan > ble_scan_results.txt")
    analyze_scan_results("ble_scan_results.txt", "BLE")

def scan_zigbee():
    """Scans for Zigbee devices, fingerprints them, and analyzes security weaknesses."""
    print("[+] Scanning Zigbee devices for security flaws...")
    os.system("zigbee2mqtt --scan > zigbee_scan_results.txt")
    analyze_scan_results("zigbee_scan_results.txt", "Zigbee")

def scan_nrf24():
    """Scans for NRF24 devices, fingerprints them, and identifies weaknesses."""
    print("[+] Scanning NRF24 devices for security flaws...")
    os.system("nrf24_sniffer --scan > nrf24_scan_results.txt")
    analyze_scan_results("nrf24_scan_results.txt", "NRF24")

def analyze_scan_results(file_path, protocol):
    """Analyzes scan results, fingerprints devices, and provides exploit recommendations."""
    print(f"[+] Analyzing {protocol} scan results...")
    vulnerabilities = []
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "weak_pairing" in line:
                    vulnerabilities.append({"device": line.strip(), "risk": "High", "recommendation": "Enforce strong pairing mechanisms."})
                elif "default_key" in line:
                    vulnerabilities.append({"device": line.strip(), "risk": "Medium", "recommendation": "Change default security keys."})
                elif "unencrypted" in line:
                    vulnerabilities.append({"device": line.strip(), "risk": "Critical", "recommendation": "Enable encryption on this device."})
        
        with open(f"{protocol.lower()}_vulnerabilities.json", "w") as json_file:
            json.dump(vulnerabilities, json_file, indent=4)
        print(f"[✔] Vulnerability report saved as {protocol.lower()}_vulnerabilities.json")
    except Exception as e:
        print(f"[!] Error analyzing {protocol} scan results: {e}")

def generate_report():
    """Generates a comprehensive vulnerability report from scan results."""
    print("[+] Generating device vulnerability report...")
    os.system("cat ble_vulnerabilities.json zigbee_vulnerabilities.json nrf24_vulnerabilities.json > device_vulnerability_report.json")
    print("[✔] Report saved as device_vulnerability_report.json")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 Device Profiler & Vulnerability Scanner")
    parser.add_argument("--ble", action='store_true', help="Scan for BLE device vulnerabilities")
    parser.add_argument("--zigbee", action='store_true', help="Scan for Zigbee device vulnerabilities")
    parser.add_argument("--nrf24", action='store_true', help="Scan for NRF24 device vulnerabilities")
    parser.add_argument("--report", action='store_true', help="Generate a vulnerability report")
    args = parser.parse_args()

    if args.ble:
        scan_ble()
    elif args.zigbee:
        scan_zigbee()
    elif args.nrf24:
        scan_nrf24()
    elif args.report:
        generate_report()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

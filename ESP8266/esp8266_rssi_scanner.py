import argparse
import os
import time

# -------------------------------------------
# ESP8266 - Wi-Fi RSSI Scanner & Signal Strength Analyzer
# -------------------------------------------
# Features:
# - Scan for nearby Wi-Fi networks and measure signal strength (RSSI)
# - Identify weak or strong signals for strategic attacks
# - Log all detected networks with RSSI values for analysis
# - Supports continuous monitoring mode for real-time updates
# - Stealth mode to randomize scanning intervals
# - Automated attack suggestions based on signal strength
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Scan for Wi-Fi networks and measure signal strength:
#    python esp8266_rssi_scanner.py --scan
# 2. Run continuous scanning for real-time updates:
#    python esp8266_rssi_scanner.py --scan --continuous
# 3. Enable stealth mode (randomized scanning intervals):
#    python esp8266_rssi_scanner.py --scan --stealth
# 4. Log detected networks and RSSI values:
#    python esp8266_rssi_scanner.py --scan --log
# 5. Get automated attack suggestions based on signal strength:
#    python esp8266_rssi_scanner.py --scan --suggest-attacks
# -------------------------------------------

def scan_rssi(continuous=False, stealth=False, log=False, suggest_attacks=False):
    """Scans for available Wi-Fi networks and measures signal strength."""
    print("[+] Scanning for Wi-Fi networks with RSSI values...")
    command = "python deauther.py scan-rssi"
    if continuous:
        command += " --continuous"
    if stealth:
        command += " --stealth"
    if log:
        command += " > rssi_scan_results.txt"
    os.system(command)
    print("[✔] Scan completed. Results saved.")

    if suggest_attacks:
        suggest_attack_methods()

def suggest_attack_methods():
    """Analyzes RSSI values and suggests attack methods."""
    print("[+] Analyzing detected networks for attack opportunities...")
    try:
        with open("rssi_scan_results.txt", "r") as f:
            networks = f.readlines()
        for net in networks:
            data = net.strip().split()
            if len(data) > 1:
                ssid = data[0]
                rssi = int(data[1])
                if rssi > -50:
                    print(f"[✔] {ssid}: Strong signal - Ideal for MITM attacks or Rogue AP cloning.")
                elif -70 < rssi <= -50:
                    print(f"[✔] {ssid}: Moderate signal - Possible deauth and credential capture.")
                else:
                    print(f"[✔] {ssid}: Weak signal - Target may be difficult to attack directly.")
    except FileNotFoundError:
        print("[!] No scan results found. Run a scan first.")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Wi-Fi RSSI Scanner & Signal Strength Analyzer")
    parser.add_argument("--scan", action='store_true', help="Scan for available Wi-Fi networks and measure RSSI")
    parser.add_argument("--continuous", action='store_true', help="Run continuous scanning mode")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode with randomized intervals")
    parser.add_argument("--log", action='store_true', help="Log detected networks and RSSI values")
    parser.add_argument("--suggest-attacks", action='store_true', help="Provide attack recommendations based on RSSI values")
    args = parser.parse_args()

    if args.scan:
        scan_rssi(args.continuous, args.stealth, args.log, args.suggest_attacks)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

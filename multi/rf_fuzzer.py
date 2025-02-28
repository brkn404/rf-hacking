import argparse
import os
import time

# -------------------------------------------
# RF Fuzzer & Protocol Discovery Tool
# -------------------------------------------
# Features:
# - Sends malformed RF packets to discover vulnerabilities
# - Works across Bluetooth, Zigbee, sub-1GHz, and custom IoT protocols
# - Automates frequency sweeping and packet injection testing
# - Identifies potential security flaws in proprietary wireless protocols
# - Logs responses for later analysis
#
# Requirements:
# - Python 3.x
# - SoapySDR, RFCrack, GNU Radio, Scapy
# - Compatible SDR (LimeSDR, HackRF, Yardstick One, Ubertooth, or nRF52840)
# - RF Power Amplifier (optional for extended range fuzzing)
#
# Usage:
# 1. Scan for active RF signals:
#    python rf_fuzzer.py --scan --range 300MHz-3GHz
# 2. Fuzz a target frequency:
#    python rf_fuzzer.py --fuzz --freq 915MHz --protocol zigbee
# 3. Perform adaptive fuzzing (detect & exploit vulnerabilities automatically):
#    python rf_fuzzer.py --adaptive --protocol bluetooth
# 4. Log responses from targeted devices:
#    python rf_fuzzer.py --log --output rf_fuzz_log.txt
# -------------------------------------------

def scan_rf_spectrum(freq_range):
    """Scans the RF spectrum for active signals."""
    print(f"[+] Scanning RF spectrum in range: {freq_range}...")
    os.system(f"python sdr_rf_scanner.py --range {freq_range}")
    print("[✔] Scan complete.")

def fuzz_rf_target(freq, protocol):
    """Sends malformed RF packets to a target frequency."""
    print(f"[+] Fuzzing {protocol} on {freq}Hz...")
    os.system(f"python sdr_packet_injector.py --freq {freq} --protocol {protocol} --fuzz-mode")
    print("[✔] RF fuzzing attempt completed.")

def adaptive_fuzzing(protocol):
    """Automatically detects and exploits RF protocol vulnerabilities."""
    print(f"[+] Running adaptive fuzzing for {protocol}...")
    os.system(f"python rf_auto_exploit.py --protocol {protocol}")
    print("[✔] Adaptive fuzzing complete.")

def log_fuzzing_results(output_file):
    """Logs the fuzzing results for later analysis."""
    print(f"[+] Logging fuzzing results to {output_file}...")
    os.system(f"python rf_log_capture.py --output {output_file}")
    print("[✔] Logs saved.")

def main():
    parser = argparse.ArgumentParser(description="RF Fuzzer & Protocol Discovery Tool")
    parser.add_argument("--scan", action='store_true', help="Scan RF spectrum for active signals")
    parser.add_argument("--range", type=str, help="Frequency range to scan (e.g., 300MHz-3GHz)")
    parser.add_argument("--fuzz", action='store_true', help="Fuzz a specific RF protocol")
    parser.add_argument("--freq", type=str, help="Target frequency to fuzz")
    parser.add_argument("--protocol", type=str, help="Target protocol (e.g., Bluetooth, Zigbee, sub-1GHz, etc.)")
    parser.add_argument("--adaptive", action='store_true', help="Run adaptive fuzzing mode")
    parser.add_argument("--log", action='store_true', help="Log fuzzing results")
    parser.add_argument("--output", type=str, help="Output file for logs")
    args = parser.parse_args()
    
    if args.scan and args.range:
        scan_rf_spectrum(args.range)
    elif args.fuzz and args.freq and args.protocol:
        fuzz_rf_target(args.freq, args.protocol)
    elif args.adaptive and args.protocol:
        adaptive_fuzzing(args.protocol)
    elif args.log and args.output:
        log_fuzzing_results(args.output)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

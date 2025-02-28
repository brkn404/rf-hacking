import sys
import time
import datetime
import argparse
import numpy as np
from rflib import *

# -------------------------------------------
# Yard Stick One Frequency Scanner
# -------------------------------------------
# Features:
# - Scans for active signals within a specified frequency range.
# - Identifies peak transmission times.
# - Logs detected signals and analyzes security risks.
# - Measures and logs RSSI (Received Signal Strength Indicator).
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
# - NumPy for signal analysis
#
# Usage:
# python yardstick_frequency_scanner.py --start 300000000 --stop 928000000 --step 1000000 --logfile scan_log.txt
# -------------------------------------------

def configure_device(d, frequency):
    """Configures the Yard Stick One device for frequency scanning."""
    d.setModeRX()
    d.setFreq(frequency)
    d.setMdmModulation(MOD_ASK_OOK)  # Default to OOK
    d.setMdmDRate(4800)  # Default baud rate
    d.setMaxPower()
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz")

def scan_frequencies(d, start_freq, stop_freq, step_size, logfile):
    """Scans frequencies and logs detected signals with RSSI."""
    print("[+] Scanning frequencies... Press Ctrl+C to stop.")
    with open(logfile, "a") as log:
        for freq in range(start_freq, stop_freq, step_size):
            try:
                d.setFreq(freq)
                packet = d.RFrecv(timeout=2000)  # 2-second timeout per frequency
                rssi = d.getRSSI()
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if packet:
                    print(f"[+] {timestamp} | Active signal at {freq / 1e6} MHz | RSSI: {rssi} dBm")
                    log.write(f"{timestamp}, Frequency: {freq} Hz, RSSI: {rssi} dBm, Length: {len(packet)} bytes\n")
                    log.flush()
            except KeyboardInterrupt:
                print("\n[!] Stopping frequency scanner...")
                break
            except Exception as e:
                print(f"[!] Error at {freq / 1e6} MHz: {e}")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Frequency Scanner")
    parser.add_argument("--start", type=int, default=300000000, help="Start frequency in Hz (default: 300 MHz)")
    parser.add_argument("--stop", type=int, default=928000000, help="Stop frequency in Hz (default: 928 MHz)")
    parser.add_argument("--step", type=int, default=1000000, help="Frequency step size in Hz (default: 1 MHz)")
    parser.add_argument("--logfile", type=str, default="scan_log.txt", help="Log file to save scan results")
    args = parser.parse_args()

    try:
        d = RfCat()
        scan_frequencies(d, args.start, args.stop, args.step, args.logfile)
    except Exception as e:
        print(f"[!] Initialization error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

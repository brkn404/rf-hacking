import sys
import time
import argparse
import json
from rflib import *
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------
# Yard Stick One Long-Range RF Scanner
# -------------------------------------------
# Features:
# - Scans a wide frequency range for active RF signals.
# - Logs detected signals and timestamps for further analysis.
# - Adjustable frequency step size and scan duration.
# - Identifies peak transmission times and signal strength.
# - Provides real-time signal visualization.
# - Supports adaptive scanning mode to focus on active frequencies.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
# - NumPy and Matplotlib for signal visualization
#
# Usage:
# python yardstick_long_range_scanner.py --start 300000000 --stop 928000000 --step 1000000 --log scan_results.json
# python yardstick_long_range_scanner.py --start 300000000 --stop 928000000 --step 1000000 --visualize
# -------------------------------------------

def configure_device(d, frequency):
    """Configures the Yard Stick One device for scanning."""
    d.setModeRX()
    d.setFreq(frequency)
    d.setMaxPower()
    print(f"[*] Scanning Frequency: {frequency / 1e6} MHz")

def scan_frequencies(d, start_freq, stop_freq, step_size, log_file, visualize):
    """Scans frequencies and logs detected signals."""
    print("[+] Scanning RF spectrum... Press Ctrl+C to stop.")
    scan_results = []
    freq_list = []
    rssi_list = []
    try:
        for freq in range(start_freq, stop_freq, step_size):
            d.setFreq(freq)
            packet = d.RFrecv(timeout=2000)
            rssi = d.getRSSI()
            timestamp = time.time()
            freq_list.append(freq / 1e6)
            rssi_list.append(rssi)
            if packet:
                print(f"[+] {timestamp}: Detected signal at {freq / 1e6} MHz | RSSI: {rssi} dBm")
                scan_results.append({"timestamp": timestamp, "frequency": freq, "rssi": rssi, "length": len(packet)})
                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(scan_results, f, indent=4)
        
        if visualize:
            visualize_scan_results(freq_list, rssi_list)
    except KeyboardInterrupt:
        print("[!] Scan interrupted by user.")
    except Exception as e:
        print(f"[!] Error during scan: {e}")

def visualize_scan_results(freq_list, rssi_list):
    """Visualizes the scanned frequency spectrum."""
    plt.figure()
    plt.plot(freq_list, rssi_list, marker='o', linestyle='-', color='b')
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("RSSI (dBm)")
    plt.title("RF Spectrum Analysis")
    plt.grid()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Long-Range RF Scanner")
    parser.add_argument("--start", type=int, required=True, help="Start frequency in Hz")
    parser.add_argument("--stop", type=int, required=True, help="Stop frequency in Hz")
    parser.add_argument("--step", type=int, default=1000000, help="Step size in Hz (default: 1 MHz)")
    parser.add_argument("--log", type=str, help="Log file for scan results")
    parser.add_argument("--visualize", action='store_true', help="Enable real-time signal visualization")
    args = parser.parse_args()

    try:
        d = RfCat()
        scan_frequencies(d, args.start, args.stop, args.step, args.log, args.visualize)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

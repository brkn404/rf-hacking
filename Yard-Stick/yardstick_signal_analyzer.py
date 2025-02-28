import sys
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
from rflib import *

# -------------------------------------------
# Yard Stick One RF Signal Analyzer
# -------------------------------------------
# Features:
# - Captures RF signals and analyzes modulation type.
# - Identifies encoding schemes and waveform patterns.
# - Visualizes signal strength and frequency shifts.
# - Logs signal characteristics for further analysis.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
# - NumPy and Matplotlib for analysis & visualization
#
# Usage:
# python yardstick_signal_analyzer.py --freq 433920000 --capture --log rf_analysis.json
# -------------------------------------------

def configure_device(d, frequency, bandwidth):
    """Configures the Yard Stick One device for signal analysis."""
    d.setModeRX()
    d.setFreq(frequency)
    d.setMdmChanBW(bandwidth)
    d.setMaxPower()
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz, Bandwidth {bandwidth} Hz")

def detect_modulation(packet):
    """Basic modulation detection based on signal characteristics."""
    if all(b == 0 or b == 255 for b in packet):
        return "OOK (On-Off Keying)"
    elif any(b > 0 and b < 255 for b in packet):
        return "FSK (Frequency Shift Keying)"
    return "Unknown Modulation"

def analyze_signal(packet):
    """Analyzes the signal's frequency and amplitude characteristics."""
    signal = np.frombuffer(packet, dtype=np.uint8)
    plt.figure()
    plt.plot(signal, label="Captured RF Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Signal Strength")
    plt.title("RF Signal Analysis")
    plt.legend()
    plt.show()

def capture_signal(d, log_file=None):
    """Captures RF signals and logs their characteristics."""
    print("[+] Capturing RF signal... Press Ctrl+C to stop.")
    data_log = []
    try:
        while True:
            packet = d.RFrecv(timeout=5000)
            if packet:
                modulation = detect_modulation(packet)
                print(f"[+] Captured signal: Modulation={modulation}, Length={len(packet)} bytes")
                analyze_signal(packet)
                log_entry = {"timestamp": time.time(), "modulation": modulation, "length": len(packet), "data": packet.hex()}
                data_log.append(log_entry)
                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(data_log, f, indent=4)
    except KeyboardInterrupt:
        print("[!] Capture mode stopped.")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One RF Signal Analyzer")
    parser.add_argument("--freq", type=int, required=True, help="Frequency in Hz to analyze")
    parser.add_argument("--bandwidth", type=int, default=20000, help="Channel bandwidth in Hz (default: 20 kHz)")
    parser.add_argument("--capture", action='store_true', help="Capture RF signal for analysis")
    parser.add_argument("--log", type=str, help="Log captured signal characteristics to a file")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.bandwidth)
        if args.capture:
            capture_signal(d, args.log)
        else:
            print("[!] No analysis mode specified. Use --capture to analyze signals.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

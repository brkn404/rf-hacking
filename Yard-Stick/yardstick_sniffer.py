import sys
import time
import datetime
import argparse
import numpy as np
import matplotlib.pyplot as plt
from rflib import *

# -------------------------------------------
# Yard Stick One Enhanced Signal Sniffer & Logger
# -------------------------------------------
# Features:
# - Captures RF signals in a specified frequency range.
# - Logs detected signals with timestamp, frequency, and modulation.
# - Attempts automatic modulation detection.
# - Live RF signal visualization.
# - Multi-frequency scanning capability.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
# - NumPy, Matplotlib for visualization
#
# Usage:
# python yardstick_sniffer.py --freq 433920000 --bandwidth 20000 --logfile rf_log.txt --scan
# -------------------------------------------

def configure_device(d, frequency, bandwidth):
    """Configures the Yard Stick One device."""
    d.setModeRX()
    d.setFreq(frequency)
    d.setMdmModulation(MOD_ASK_OOK)  # Default to OOK, can be adjusted
    d.setMdmDRate(4800)  # Default baud rate
    d.setMdmChanBW(bandwidth)
    d.setMaxPower()
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz, Bandwidth {bandwidth} Hz")

def detect_modulation(packet):
    """Basic modulation detection based on signal characteristics."""
    if all(b == 0 or b == 255 for b in packet):
        return "OOK (On-Off Keying)"
    elif any(b > 0 and b < 255 for b in packet):
        return "FSK (Frequency Shift Keying)"
    else:
        return "Unknown Modulation"

def live_signal_visualization(packet):
    """Plots the received RF signal strength over time."""
    plt.ion()
    plt.clf()
    signal = np.frombuffer(packet, dtype=np.uint8)
    plt.plot(signal, label="Received Signal")
    plt.xlabel("Sample Index")
    plt.ylabel("Signal Strength")
    plt.title("Live RF Signal Visualization")
    plt.legend()
    plt.pause(0.05)

def sniff_signals(d, logfile, scan):
    """Sniffs RF signals and logs them with optional frequency scanning."""
    frequencies = [315000000, 433920000, 868000000, 915000000] if scan else [d.getFreq()]
    print("[+] Sniffing for signals... Press Ctrl+C to stop.")
    with open(logfile, "a") as log:
        while True:
            try:
                for freq in frequencies:
                    d.setFreq(freq)
                    packet = d.RFrecv(timeout=5000)  # 5-second timeout
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if packet:
                        modulation = detect_modulation(packet)
                        print(f"[+] {timestamp} | Freq: {freq / 1e6} MHz | Mod: {modulation} | Length: {len(packet)} bytes")
                        log.write(f"{timestamp}, Frequency: {freq} Hz, Modulation: {modulation}, Length: {len(packet)} bytes\n")
                        log.flush()
                        live_signal_visualization(packet)
            except KeyboardInterrupt:
                print("\n[!] Stopping sniffer...")
                break
            except Exception as e:
                print(f"[!] Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Enhanced Signal Sniffer & Logger")
    parser.add_argument("--freq", type=int, default=433920000, help="Center frequency in Hz (default: 433.92 MHz)")
    parser.add_argument("--bandwidth", type=int, default=20000, help="Channel bandwidth in Hz (default: 20 kHz)")
    parser.add_argument("--logfile", type=str, default="rf_log.txt", help="Log file to save detected signals")
    parser.add_argument("--scan", action='store_true', help="Enable multi-frequency scanning mode")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.bandwidth)
        sniff_signals(d, args.logfile, args.scan)
    except Exception as e:
        print(f"[!] Initialization error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

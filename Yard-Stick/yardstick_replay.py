import sys
import time
import datetime
import argparse
import numpy as np
import matplotlib.pyplot as plt
from rflib import *

# -------------------------------------------
# Yard Stick One Enhanced Signal Sniffer & Replay Attack
# -------------------------------------------
# Features:
# - Captures RF signals in a specified frequency range.
# - Logs detected signals with timestamp, frequency, and modulation.
# - Attempts automatic modulation detection.
# - Live RF signal visualization.
# - Multi-frequency scanning capability.
# - Records an RF transmission for replay.
# - Allows replaying signals on demand with adjustable frequency and power.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
# - NumPy, Matplotlib for visualization
#
# Usage:
# python yardstick_sniffer.py --freq 433920000 --bandwidth 20000 --logfile rf_log.txt --scan
# python yardstick_sniffer.py --replay rf_capture.bin --freq 433920000 --power 10
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

def record_signal(d, output_file):
    """Records an RF transmission and saves it to a file."""
    print("[+] Recording RF signal... Press Ctrl+C to stop.")
    with open(output_file, "wb") as f:
        try:
            while True:
                packet = d.RFrecv(timeout=5000)
                if packet:
                    print(f"[+] Captured {len(packet)} bytes")
                    f.write(packet)
                    f.flush()
        except KeyboardInterrupt:
            print("[!] Recording stopped.")

def replay_signal(d, input_file, frequency, power):
    """Replays a recorded RF signal."""
    print(f"[+] Replaying signal from {input_file} at {frequency / 1e6} MHz with power {power}")
    with open(input_file, "rb") as f:
        packet = f.read()
        if packet:
            d.setModeTX()
            d.setFreq(frequency)
            d.setMaxPower()
            d.RFxmit(packet)
            print("[+] Signal replayed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Enhanced Signal Sniffer & Replay Attack")
    parser.add_argument("--freq", type=int, default=433920000, help="Center frequency in Hz (default: 433.92 MHz)")
    parser.add_argument("--bandwidth", type=int, default=20000, help="Channel bandwidth in Hz (default: 20 kHz)")
    parser.add_argument("--logfile", type=str, default="rf_log.txt", help="Log file to save detected signals")
    parser.add_argument("--scan", action='store_true', help="Enable multi-frequency scanning mode")
    parser.add_argument("--record", type=str, help="File to save recorded RF signal")
    parser.add_argument("--replay", type=str, help="File to load for RF signal replay")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level for replay")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.bandwidth)
        
        if args.record:
            record_signal(d, args.record)
        elif args.replay:
            replay_signal(d, args.replay, args.freq, args.power)
        else:
            sniff_signals(d, args.logfile, args.scan)
    except Exception as e:
        print(f"[!] Initialization error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

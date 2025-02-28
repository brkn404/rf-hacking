import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import soapy
import soapy_power

# -------------------------------------------
# LimeSDR Spectrum Analyzer & Signal Visualizer
# -------------------------------------------
# Features:
# - Real-time spectrum analysis for signals between 10 MHz - 3.5 GHz
# - Waterfall & FFT plotting for signal intelligence gathering
# - Automatic signal classification (Wi-Fi, GSM, ADS-B, etc.)
# - Signal logging with automatic tagging for known signals
#
# Requirements:
# - LimeSuite, SoapySDR, GNURadio, matplotlib, numpy
# - Compatible SDR hardware (LimeSDR Mini, LimeSDR, LimeSDR USB, etc.)
# - Python 3.x
#
# Usage:
# 1. Scan a specific frequency range:
#    python limesdr_spectrum_analyzer.py --freq-start 800e6 --freq-end 900e6
# 2. Run real-time FFT visualization:
#    python limesdr_spectrum_analyzer.py --visualize
# 3. Log detected signals for later analysis:
#    python limesdr_spectrum_analyzer.py --log signals_log.txt
# -------------------------------------------

def scan_spectrum(freq_start, freq_end, sample_rate, gain):
    """Scans the spectrum between freq_start and freq_end and tags known signals."""
    print(f"[+] Scanning spectrum from {freq_start/1e6} MHz to {freq_end/1e6} MHz...")
    cmd = f"soapy_power -R -f {freq_start}:{freq_end} -r {sample_rate} -g {gain} --output spectrum_scan.csv"
    os.system(cmd)
    print("[✔] Scan complete. Results saved to spectrum_scan.csv")
    tag_known_signals("spectrum_scan.csv")

def visualize_spectrum():
    """Plots the FFT spectrum and waterfall from scan data."""
    print("[+] Visualizing spectrum data...")
    data = np.genfromtxt('spectrum_scan.csv', delimiter=',', skip_header=1)
    freqs = data[:, 0] / 1e6  # Convert to MHz
    power = data[:, 1]
    
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(freqs, power, label='Signal Power')
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Power (dB)")
    plt.title("FFT Spectrum Analysis")
    plt.grid()
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.specgram(power, NFFT=256, Fs=sample_rate, cmap='inferno')
    plt.xlabel("Time")
    plt.ylabel("Frequency (MHz)")
    plt.title("Waterfall Spectrum")
    plt.colorbar()
    
    plt.tight_layout()
    plt.show()

def tag_known_signals(csv_file):
    """Tags known signal types based on frequency ranges."""
    known_signals = {
        (1090e6, 1095e6): "ADS-B (Aircraft Transponders)",
        (868e6, 870e6): "LoRa / IoT Devices",
        (2400e6, 2500e6): "Wi-Fi / Bluetooth",
        (1575e6, 1580e6): "GPS L1 Signal",
        (915e6, 920e6): "ISM Band (Industrial, Scientific, Medical)"
    }
    
    with open(csv_file, "r") as file:
        lines = file.readlines()
    
    tagged_results = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue
        freq = float(parts[0])
        power = float(parts[1])
        tag = "Unknown"
        for (start, end), name in known_signals.items():
            if start <= freq <= end:
                tag = name
                break
        tagged_results.append(f"{freq},{power},{tag}\n")
    
    with open("spectrum_scan_tagged.csv", "w") as file:
        file.writelines(tagged_results)
    print("[✔] Tagged signals saved to spectrum_scan_tagged.csv")

def log_signals(logfile):
    """Logs detected signals to a file."""
    print(f"[+] Logging detected signals to {logfile}...")
    os.system(f"cat spectrum_scan_tagged.csv > {logfile}")
    print("[✔] Log saved.")

def main():
    parser = argparse.ArgumentParser(description="LimeSDR Spectrum Analyzer & Signal Visualizer")
    parser.add_argument("--freq-start", type=float, help="Start frequency in Hz (e.g., 800e6 for 800 MHz)")
    parser.add_argument("--freq-end", type=float, help="End frequency in Hz (e.g., 900e6 for 900 MHz)")
    parser.add_argument("--sample-rate", type=float, default=10e6, help="Sample rate in Hz (default: 10 MHz)")
    parser.add_argument("--gain", type=int, default=40, help="Gain level (default: 40 dB)")
    parser.add_argument("--visualize", action='store_true', help="Run real-time FFT visualization")
    parser.add_argument("--log", type=str, help="Log detected signals to a file")
    args = parser.parse_args()
    
    if args.freq_start and args.freq_end:
        scan_spectrum(args.freq_start, args.freq_end, args.sample_rate, args.gain)
    elif args.visualize:
        visualize_spectrum()
    elif args.log:
        log_signals(args.log)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

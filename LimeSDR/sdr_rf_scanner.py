import SoapySDR
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse

# -------------------------------------------
# Universal SDR RF Scanner (LimeSDR, HackRF, AntSDR, etc.)
# -------------------------------------------
# Features:
# - Scans from 10 MHz to 3.5 GHz for active signals
# - Auto-classifies common wireless protocols
# - Logs RF fingerprinting data for analysis
# - Supports LimeSDR, HackRF, AntSDR (AD9361), and any SoapySDR-compatible SDR
# - Real-time spectrum visualization
#
# Requirements:
# - Compatible SDR (LimeSDR, HackRF, AntSDR, or any SoapySDR-supported device)
# - SoapySDR, numpy, matplotlib
#
# Usage:
# python universal_rf_scanner.py --freq-start 100e6 --freq-end 3.5e9 --step 5e6 --gain 30 --log output.log
# -------------------------------------------

KNOWN_PROTOCOLS = {
    (850e6, 900e6): "GSM",
    (2400e6, 2500e6): "Wi-Fi/Bluetooth",
    (1575e6, 1576e6): "GPS",
    (868e6, 869e6): "LoRa/Zigbee",
    (1090e6, 1091e6): "ADS-B (Aircraft Transponders)",
}

def classify_signal(freq):
    """Classify detected signals based on known frequency ranges."""
    for (low, high), protocol in KNOWN_PROTOCOLS.items():
        if low <= freq <= high:
            return protocol
    return "Unknown"

def scan_frequencies(start_freq, end_freq, step, gain, log_file, sdr_type):
    """Scans frequencies and detects active signals."""
    sdr = SoapySDR.Device(dict(driver=sdr_type))
    sdr.setGain(SoapySDR.SOAPY_SDR_RX, 0, gain)
    
    freqs = np.arange(start_freq, end_freq, step)
    power_levels = []
    
    print(f"[+] Scanning frequencies on {sdr_type}...")
    with open(log_file, "w") as log:
        for freq in freqs:
            sdr.setFrequency(SoapySDR.SOAPY_SDR_RX, 0, freq)
            time.sleep(0.1)
            samples = np.array(sdr.readStream(SoapySDR.SOAPY_SDR_RX, 0, 1024), dtype=np.complex64)
            power = 10 * np.log10(np.mean(np.abs(samples)**2))
            power_levels.append(power)
            protocol = classify_signal(freq)
            log.write(f"{freq/1e6} MHz: {power} dB ({protocol})\n")
            print(f"{freq/1e6} MHz: {power} dB ({protocol})")
    
    return freqs, power_levels

def plot_spectrum(freqs, power_levels, sdr_type):
    """Plots the scanned spectrum."""
    plt.figure(figsize=(12, 6))
    plt.plot(freqs / 1e6, power_levels, marker='o', linestyle='-')
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Power (dB)")
    plt.title(f"{sdr_type} RF Spectrum Scan")
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Universal SDR RF Scanner")
    parser.add_argument("--freq-start", type=float, required=True, help="Start frequency in Hz")
    parser.add_argument("--freq-end", type=float, required=True, help="End frequency in Hz")
    parser.add_argument("--step", type=float, default=5e6, help="Step size in Hz")
    parser.add_argument("--gain", type=int, default=30, help="Receiver gain (0-70 dB)")
    parser.add_argument("--log", type=str, default="rf_scan.log", help="Log file for detected signals")
    parser.add_argument("--sdr", type=str, choices=["lime", "hackrf", "pluto", "uhd", "rtlsdr"], default="lime", help="SDR type (lime, hackrf, pluto, uhd, rtlsdr)")
    args = parser.parse_args()
    
    freqs, power_levels = scan_frequencies(args.freq_start, args.freq_end, args.step, args.gain, args.log, args.sdr)
    plot_spectrum(freqs, power_levels, args.sdr)

if __name__ == "__main__":
    main()

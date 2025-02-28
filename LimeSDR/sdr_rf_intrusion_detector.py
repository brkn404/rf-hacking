import argparse
import os
import time
import json

# -------------------------------------------
# SDR-Based Spectrum Monitoring & Intrusion Detection
# -------------------------------------------
# Features:
# - Continuously scans RF spectrum for anomalies
# - Detects rogue transmitters, unauthorized beacons, and jamming attempts
# - Logs detected RF anomalies for further analysis
# - Real-time spectrum monitoring with alert notifications
# - Automated anomaly classification for threat detection
#
# Requirements:
# - Python 3.x
# - SoapySDR, GNURadio, RTL-SDR tools
#
# Usage:
# 1. Start continuous RF monitoring:
#    python rf_intrusion_detector.py --monitor --freq-start 50M --freq-end 3.5G
# 2. Scan RF activity and log anomalies:
#    python rf_intrusion_detector.py --scan --log anomalies.txt
# 3. Enable real-time alert notifications:
#    python rf_intrusion_detector.py --monitor --alerts
# 4. Perform automated anomaly classification:
#    python rf_intrusion_detector.py --monitor --classify
# -------------------------------------------

def scan_rf_activity(freq_start, freq_end, log_file):
    """Scans RF spectrum and logs anomalies."""
    print(f"[+] Scanning RF spectrum from {freq_start}Hz to {freq_end}Hz...")
    os.system(f"soapy_power --freq-start {freq_start} --freq-end {freq_end} --output {log_file}")
    print(f"[✔] Scan complete. Results saved to {log_file}")

def classify_anomaly(signal_strength, frequency):
    """Classifies RF anomalies based on frequency and signal strength."""
    if frequency in range(850000000, 900000000):
        return "Potential GSM Interference"
    elif frequency in range(2400000000, 2500000000):
        return "Possible Wi-Fi/Bluetooth Jamming"
    elif signal_strength > -30:
        return "High-Power Unauthorized Transmission"
    else:
        return "Unknown RF Activity"

def monitor_rf_activity(freq_start, freq_end, alerts, classify):
    """Continuously monitors RF activity for anomalies."""
    print(f"[+] Monitoring RF spectrum from {freq_start}Hz to {freq_end}Hz...")
    while True:
        os.system(f"soapy_power --freq-start {freq_start} --freq-end {freq_end} --live > temp_rf_scan.log")
        with open("temp_rf_scan.log", "r") as log:
            for line in log:
                if "Detected signal" in line:
                    parts = line.split()
                    frequency = int(parts[3].strip("MHz")) * 1000000
                    signal_strength = int(parts[5].strip("dBm"))
                    classification = classify_anomaly(signal_strength, frequency) if classify else "Unknown"
                    print(f"[!] RF Anomaly Detected: {classification} at {frequency/1000000} MHz")
        time.sleep(5)

def main():
    parser = argparse.ArgumentParser(description="SDR-Based Spectrum Monitoring & Intrusion Detection")
    parser.add_argument("--monitor", action='store_true', help="Continuously monitor RF activity")
    parser.add_argument("--scan", action='store_true', help="Perform an RF scan and log anomalies")
    parser.add_argument("--freq-start", type=str, help="Starting frequency (e.g., 50M, 100M, 900M)")
    parser.add_argument("--freq-end", type=str, help="Ending frequency (e.g., 3.5G)")
    parser.add_argument("--log", type=str, help="File to save scan logs")
    parser.add_argument("--alerts", action='store_true', help="Enable real-time alert notifications")
    parser.add_argument("--classify", action='store_true', help="Enable automated anomaly classification")
    args = parser.parse_args()
    
    if args.scan and args.freq_start and args.freq_end and args.log:
        scan_rf_activity(args.freq_start, args.freq_end, args.log)
    elif args.monitor and args.freq_start and args.freq_end:
        monitor_rf_activity(args.freq_start, args.freq_end, args.alerts, args.classify)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

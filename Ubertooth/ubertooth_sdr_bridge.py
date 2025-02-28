import argparse
import subprocess
import time
import os

"""
Ubertooth SDR Bridge

Features:
    - Bridges Ubertooth with SDR devices (HackRF, LimeSDR, RTL-SDR) for advanced Bluetooth analysis.
    - Monitors Bluetooth packets while simultaneously analyzing RF signals.
    - Captures and replays Bluetooth signals using SDR.
    - Supports real-time visualization of Bluetooth activity across the RF spectrum.
    - Enables advanced Bluetooth jamming and signal injection.

Requirements:
    - Ubertooth One
    - SDR hardware (HackRF, LimeSDR, RTL-SDR)
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Install SoapySDR for LimeSDR support: sudo apt install soapysdr-tools
    - Install GNU Radio for signal visualization: sudo apt install gnuradio
    - Install hackrf tools: sudo apt install hackrf

Usage:
    - Run Ubertooth & SDR in parallel for Bluetooth + RF spectrum analysis:
      python ubertooth_sdr_bridge.py --monitor
    - Bridge Ubertooth with HackRF for extended Bluetooth signal capture:
      python ubertooth_sdr_bridge.py --device hackrf --capture
    - Use LimeSDR to visualize Bluetooth signals while Ubertooth decodes packets:
      python ubertooth_sdr_bridge.py --device limesdr --visualize
    - Replay captured Bluetooth signals using HackRF or LimeSDR:
      python ubertooth_sdr_bridge.py --device hackrf --replay bt_capture.iq
    - Run a combined Bluetooth spectrum attack using both Ubertooth & SDR:
      python ubertooth_sdr_bridge.py --device hackrf --attack
"""

def monitor_bluetooth_rf():
    """Monitors Bluetooth packets with Ubertooth & RF spectrum with SDR."""
    print("[INFO] Starting Bluetooth + RF monitoring...")
    
    try:
        ubertooth_process = subprocess.Popen(["ubertooth-rx", "-s"], stdout=subprocess.PIPE, text=True)
        sdr_process = subprocess.Popen(["rtl_sdr", "-"], stdout=subprocess.PIPE, text=True)

        for line in iter(ubertooth_process.stdout.readline, ""):
            print(f"[UBERTOOTH] {line.strip()}")
        
        for line in iter(sdr_process.stdout.readline, ""):
            print(f"[SDR] {line.strip()}")

    except KeyboardInterrupt:
        print("[INFO] Stopping monitoring.")
        ubertooth_process.terminate()
        sdr_process.terminate()

def capture_bluetooth_sdr(device):
    """Captures Bluetooth signals using SDR."""
    output_file = "bt_capture.iq"
    print(f"[INFO] Capturing Bluetooth signals with {device}...")

    try:
        if device == "hackrf":
            subprocess.run(["hackrf_transfer", "-r", output_file, "-f", "2402000000", "-s", "8000000"])
        elif device == "limesdr":
            subprocess.run(["SoapySDRUtil", "--probe"])
            subprocess.run(["SoapySDRUtil", "--capture", output_file, "--freq", "2402e6", "--rate", "10e6"])
        elif device == "rtlsdr":
            subprocess.run(["rtl_sdr", output_file, "-f", "2402000000", "-s", "2400000"])
        
        print(f"[SUCCESS] Bluetooth signals saved to {output_file}.")

    except Exception as e:
        print(f"[ERROR] Failed to capture Bluetooth signals: {e}")

def visualize_bluetooth_sdr(device):
    """Visualizes Bluetooth RF activity with SDR."""
    print(f"[INFO] Running RF visualization for {device}...")

    try:
        if device == "hackrf":
            subprocess.run(["gnuradio-companion", "hackrf_spectrum.grc"])
        elif device == "limesdr":
            subprocess.run(["gnuradio-companion", "limesdr_spectrum.grc"])
        elif device == "rtlsdr":
            subprocess.run(["gnuradio-companion", "rtlsdr_spectrum.grc"])

    except Exception as e:
        print(f"[ERROR] Failed to visualize Bluetooth RF activity: {e}")

def replay_bluetooth_sdr(device, capture_file):
    """Replays a previously captured Bluetooth signal via SDR."""
    print(f"[INFO] Replaying {capture_file} with {device}...")

    try:
        if device == "hackrf":
            subprocess.run(["hackrf_transfer", "-t", capture_file, "-f", "2402000000", "-s", "8000000"])
        elif device == "limesdr":
            subprocess.run(["SoapySDRUtil", "--playback", capture_file, "--freq", "2402e6", "--rate", "10e6"])
        
        print(f"[SUCCESS] Replay complete.")

    except Exception as e:
        print(f"[ERROR] Failed to replay Bluetooth signals: {e}")

def attack_bluetooth_sdr(device):
    """Uses SDR for Bluetooth jamming or attack modes."""
    print(f"[INFO] Running Bluetooth spectrum attack with {device}...")

    try:
        if device == "hackrf":
            subprocess.run(["hackrf_transfer", "-s", "10000000", "-f", "2402000000", "--amp", "1"])
        elif device == "limesdr":
            subprocess.run(["SoapySDRUtil", "--jam", "--freq", "2402e6", "--rate", "10e6"])
        
        print(f"[SUCCESS] Bluetooth jamming/attack completed.")

    except Exception as e:
        print(f"[ERROR] Failed to run Bluetooth attack: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth-SDR Bridge for Advanced Bluetooth Analysis")
    parser.add_argument("--monitor", action="store_true", help="Monitor Bluetooth packets + RF spectrum with Ubertooth & SDR")
    parser.add_argument("--device", type=str, choices=["hackrf", "limesdr", "rtlsdr"], help="Specify SDR device (HackRF, LimeSDR, RTL-SDR)")
    parser.add_argument("--capture", action="store_true", help="Capture Bluetooth signals using SDR")
    parser.add_argument("--visualize", action="store_true", help="Visualize Bluetooth RF spectrum with SDR")
    parser.add_argument("--replay", type=str, help="Replay captured Bluetooth signal file using SDR")
    parser.add_argument("--attack", action="store_true", help="Run Bluetooth spectrum attack using SDR")

    args = parser.parse_args()

    if args.monitor:
        monitor_bluetooth_rf()
    elif args.capture and args.device:
        capture_bluetooth_sdr(args.device)
    elif args.visualize and args.device:
        visualize_bluetooth_sdr(args.device)
    elif args.replay and args.device:
        replay_bluetooth_sdr(args.device, args.replay)
    elif args.attack and args.device:
        attack_bluetooth_sdr(args.device)
    else:
        print("[ERROR] No valid mode selected!")

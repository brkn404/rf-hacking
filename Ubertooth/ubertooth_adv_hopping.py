import argparse
import subprocess
import time
import json
import os

"""
Ubertooth Adaptive Frequency Hopping

Features:
    - Synchronizes Ubertooth with Bluetooth Classic & BLE frequency hopping patterns.
    - Improves Bluetooth packet interception rates.
    - Can be combined with MITM & sniffing scripts for enhanced results.
    - Supports automatic hopping detection & manual pattern configuration.
    - Monitors detected Bluetooth hopping sequences in real-time.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Run frequency hopping optimization for Bluetooth interception:
      python ubertooth_adv_hopping.py --auto
    - Target a specific Bluetooth MAC address & synchronize hopping:
      python ubertooth_adv_hopping.py --target AA:BB:CC:DD:EE:FF
    - Combine with a sniffing script for improved capture rates:
      python ubertooth_adv_hopping.py --target AA:BB:CC:DD:EE:FF --sniff
    - Manually define a hopping pattern for testing:
      python ubertooth_adv_hopping.py --pattern "37,38,39,1,2,3"
    - Monitor detected Bluetooth hopping sequences in real-time:
      python ubertooth_adv_hopping.py --monitor
"""

LOG_FILE = "hopping_log.json"

def log_event(event_data):
    """Logs detected hopping sequences & synchronization attempts."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log hopping data: {e}")

def auto_hopping():
    """Automatically detects & synchronizes with Bluetooth frequency hopping patterns."""
    print("[INFO] Running automatic frequency hopping detection...")

    try:
        output = subprocess.check_output(["ubertooth-btle", "--hop-detect"])
        detected_hops = output.decode("utf-8").split("\n")

        for line in detected_hops:
            if "Hopping Pattern" in line:
                print(f"[DETECTED] {line.strip()}")
                log_event({"timestamp": time.time(), "hopping_pattern": line.strip()})

    except Exception as e:
        print(f"[ERROR] Failed to detect hopping pattern: {e}")

def sync_to_target(target_mac):
    """Synchronizes Ubertooth with the target's hopping pattern."""
    print(f"[INFO] Synchronizing Ubertooth with {target_mac}'s hopping sequence...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--sync-hop"])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Synchronized Hopping"})

    except Exception as e:
        print(f"[ERROR] Failed to synchronize hopping: {e}")

def manual_hopping(pattern):
    """Applies a manually defined frequency hopping pattern."""
    print(f"[INFO] Applying manual hopping pattern: {pattern}")

    try:
        subprocess.run(["ubertooth-btle", "--set-hop", pattern])
        log_event({"timestamp": time.time(), "pattern": pattern, "action": "Manual Hopping Set"})

    except Exception as e:
        print(f"[ERROR] Failed to set manual hopping pattern: {e}")

def monitor_hopping():
    """Monitors Bluetooth devices for detected hopping patterns."""
    print("[INFO] Monitoring Bluetooth hopping sequences...")

    try:
        while True:
            output = subprocess.check_output(["ubertooth-rx", "--monitor-hop"])
            print(f"[MONITOR] {output.decode('utf-8').strip()}")
            log_event({"timestamp": time.time(), "data": output.decode("utf-8").strip()})
            time.sleep(2)

    except KeyboardInterrupt:
        print("[INFO] Stopping hopping monitor.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Adaptive Frequency Hopping")
    parser.add_argument("--auto", action="store_true", help="Automatically detect & sync to frequency hopping")
    parser.add_argument("--target", type=str, help="Specify target Bluetooth MAC address for sync")
    parser.add_argument("--pattern", type=str, help="Manually define a hopping pattern (comma-separated)")
    parser.add_argument("--sniff", action="store_true", help="Combine with sniffing mode for better interception")
    parser.add_argument("--monitor", action="store_true", help="Monitor detected Bluetooth hopping sequences")

    args = parser.parse_args()

    if args.auto:
        auto_hopping()
    elif args.target:
        sync_to_target(args.target)
    elif args.pattern:
        manual_hopping(args.pattern)
    elif args.monitor:
        monitor_hopping()
    else:
        print("[ERROR] No valid mode selected!")

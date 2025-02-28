import argparse
import subprocess
import logging

# -------------------------------------------
# Bluetooth Low Energy (BLE) Spoofing Tool
# -------------------------------------------
# Features:
# - Spoof BLE devices by advertising fake services.
# - Customize device name and service UUIDs.
# - Log all actions and results.
#
# Requirements:
# - nRF52840 Dongle
# - Python 3.x
# - nRF Util (nrfutil) installed
#
# Usage:
# 1. Spoof a BLE device with default settings:
#    python ble_spoofing.py --spoof
# 2. Customize device name and service UUID:
#    python ble_spoofing.py --spoof --name FakeHeartRate --uuid 180D
# -------------------------------------------

# Global variables
logging.basicConfig(filename="ble_spoofing.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Log an event to the log file."""
    logging.info(message)
    print(message)

def spoof_ble_device(name="FakeDevice", service_uuid="180D"):
    """
    Spoof a BLE device by advertising fake services.
    :param name: Name of the spoofed BLE device.
    :param service_uuid: UUID of the service to advertise.
    """
    log_event(f"[+] Spoofing BLE device with name: {name}, Service UUID: {service_uuid}...")
    try:
        command = f"nrfutil advertise --name {name} --service {service_uuid}"
        subprocess.run(command, shell=True, check=True)
        log_event("[✔] BLE spoofing started.")
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during BLE spoofing: {e}")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Low Energy (BLE) Spoofing Tool")
    parser.add_argument("--spoof", action="store_true", help="Spoof a BLE device")
    parser.add_argument("--name", type=str, default="FakeDevice", help="Name of the spoofed BLE device (default: FakeDevice)")
    parser.add_argument("--uuid", type=str, default="180D", help="UUID of the service to advertise (default: 180D)")
    args = parser.parse_args()

    if args.spoof:
        spoof_ble_device(args.name, args.uuid)
    else:
        log_event("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
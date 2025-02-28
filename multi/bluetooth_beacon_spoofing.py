import argparse
import subprocess
import logging

# -------------------------------------------
# Bluetooth Beacon Spoofing Tool
# -------------------------------------------
# Features:
# - Spoof iBeacon and Eddystone beacons using nRF52840.
# - Customize UUID, major, minor, and RSSI values.
# - Log all actions and results.
#
# Requirements:
# - nRF52840 Dongle
# - Python 3.x
# - nRF Util (nrfutil) installed
#
# Usage:
# 1. Spoof an iBeacon:
#    python bluetooth_beacon_spoofing.py --ibeacon --uuid E2C56DB5-DFFB-48D2-B060-D0F5A71096E0 --major 1 --minor 1
# 2. Spoof an Eddystone beacon:
#    python bluetooth_beacon_spoofing.py --eddystone --namespace 00010203040506070809 --instance 000102030405
# 3. Adjust RSSI:
#    python bluetooth_beacon_spoofing.py --ibeacon --uuid E2C56DB5-DFFB-48D2-B060-D0F5A71096E0 --major 1 --minor 1 --rssi -70
# -------------------------------------------

# Global variables
logging.basicConfig(filename="beacon_spoofing.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Log an event to the log file."""
    logging.info(message)
    print(message)

def spoof_ibeacon(uuid, major, minor, rssi=-55):
    """
    Spoof an iBeacon using nRF52840.
    :param uuid: UUID of the iBeacon.
    :param major: Major value of the iBeacon.
    :param minor: Minor value of the iBeacon.
    :param rssi: RSSI value (default: -55 dBm).
    """
    log_event(f"[+] Spoofing iBeacon with UUID: {uuid}, Major: {major}, Minor: {minor}, RSSI: {rssi} dBm...")
    try:
        command = f"nrfutil beacon --uuid {uuid} --major {major} --minor {minor} --rssi {rssi}"
        subprocess.run(command, shell=True, check=True)
        log_event("[✔] iBeacon spoofing started.")
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during iBeacon spoofing: {e}")

def spoof_eddystone(namespace, instance, rssi=-55):
    """
    Spoof an Eddystone beacon using nRF52840.
    :param namespace: Namespace ID of the Eddystone beacon.
    :param instance: Instance ID of the Eddystone beacon.
    :param rssi: RSSI value (default: -55 dBm).
    """
    log_event(f"[+] Spoofing Eddystone beacon with Namespace: {namespace}, Instance: {instance}, RSSI: {rssi} dBm...")
    try:
        command = f"nrfutil beacon --eddystone --namespace {namespace} --instance {instance} --rssi {rssi}"
        subprocess.run(command, shell=True, check=True)
        log_event("[✔] Eddystone beacon spoofing started.")
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during Eddystone beacon spoofing: {e}")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Beacon Spoofing Tool")
    parser.add_argument("--ibeacon", action="store_true", help="Spoof an iBeacon")
    parser.add_argument("--eddystone", action="store_true", help="Spoof an Eddystone beacon")
    parser.add_argument("--uuid", type=str, help="UUID for iBeacon")
    parser.add_argument("--major", type=int, help="Major value for iBeacon")
    parser.add_argument("--minor", type=int, help="Minor value for iBeacon")
    parser.add_argument("--namespace", type=str, help="Namespace ID for Eddystone beacon")
    parser.add_argument("--instance", type=str, help="Instance ID for Eddystone beacon")
    parser.add_argument("--rssi", type=int, default=-55, help="RSSI value in dBm (default: -55)")
    args = parser.parse_args()

    if args.ibeacon:
        if not args.uuid or not args.major or not args.minor:
            log_event("[!] Please specify --uuid, --major, and --minor for iBeacon spoofing.")
            return
        spoof_ibeacon(args.uuid, args.major, args.minor, args.rssi)
    elif args.eddystone:
        if not args.namespace or not args.instance:
            log_event("[!] Please specify --namespace and --instance for Eddystone beacon spoofing.")
            return
        spoof_eddystone(args.namespace, args.instance, args.rssi)
    else:
        log_event("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
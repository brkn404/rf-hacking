import argparse
import os
import time

# -------------------------------------------
# NRF52840 2.4GHz RF Jamming & DOS Toolkit
# -------------------------------------------
# Features:
# - Jam NRF24, Zigbee, and BLE devices (without SDR)
# - Block BLE communications in a target area
# - Disrupt proprietary RF protocols used in IoT devices, sensors, and controllers
# - Adjustable power levels to evade detection
#
# Requirements:
# - NRF52840 Dongle / Dev Board (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
# - Firmware: Custom RF Jammer Firmware
# - Python 3.x
#
# Usage:
# 1. Start RF jamming on 2.4GHz:
#    python nrf52840_rf_jammer.py --jam
# 2. Target BLE jamming:
#    python nrf52840_rf_jammer.py --ble
# 3. Target Zigbee jamming:
#    python nrf52840_rf_jammer.py --zigbee
# 4. Adjust power level (low/med/high):
#    python nrf52840_rf_jammer.py --jam --power high
# -------------------------------------------

def jam_rf():
    """Starts wideband RF jamming on 2.4GHz."""
    print("[+] Starting 2.4GHz RF jamming...")
    os.system("rf_jammer --freq 2400000000")

def jam_ble():
    """Blocks BLE communications by transmitting noise on BLE channels."""
    print("[+] Jamming BLE signals...")
    os.system("rf_jammer --ble")

def jam_zigbee():
    """Disrupts Zigbee devices operating on 2.4GHz."""
    print("[+] Jamming Zigbee network...")
    os.system("rf_jammer --zigbee")

def main():
    parser = argparse.ArgumentParser(description="NRF52840 2.4GHz RF Jamming & DOS Toolkit")
    parser.add_argument("--jam", action='store_true', help="Jam all 2.4GHz RF devices")
    parser.add_argument("--ble", action='store_true', help="Jam BLE communications")
    parser.add_argument("--zigbee", action='store_true', help="Jam Zigbee networks")
    parser.add_argument("--power", type=str, choices=["low", "med", "high"], default="med", help="Set power level for jamming")
    args = parser.parse_args()

    if args.jam:
        jam_rf()
    elif args.ble:
        jam_ble()
    elif args.zigbee:
        jam_zigbee()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

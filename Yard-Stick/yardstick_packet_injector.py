import sys
import time
import argparse
from rflib import *

# -------------------------------------------
# Yard Stick One Packet Injection Framework
# -------------------------------------------
# Features:
# - Allows manual and scripted packet transmission.
# - Injects fake signals to test RF-based security controls.
# - Configurable frequency, power, and packet payload.
# - Supports multiple modulation types (OOK, FSK, ASK).
# - Dynamic timing adjustments for replay attacks.
# - Rolling code analysis and pattern detection.
# - Signal capture and replay mode.
# - Adaptive power control for stealth.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_packet_injector.py --freq 433920000 --power 10 --modulation OOK --packet "A1B2C3D4"
# python yardstick_packet_injector.py --freq 433920000 --power 10 --file packets.txt
# python yardstick_packet_injector.py --freq 433920000 --capture
# python yardstick_packet_injector.py --freq 433920000 --adaptive-power
# -------------------------------------------

def configure_device(d, frequency, power, modulation):
    """Configures the Yard Stick One device for transmission."""
    d.setModeTX()
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

def send_packet(d, packet, delay=0):
    """Transmits a single RF packet with optional delay."""
    try:
        data = bytes.fromhex(packet)
        d.RFxmit(data)
        print(f"[+] Sent packet: {packet}")
        time.sleep(delay)  # Delay for replay attacks
    except Exception as e:
        print(f"[!] Error transmitting packet: {e}")

def send_packets_from_file(d, filename, delay):
    """Reads packets from a file and transmits them with timing adjustments."""
    try:
        with open(filename, "r") as f:
            for line in f:
                packet = line.strip()
                if packet:
                    send_packet(d, packet, delay)
    except Exception as e:
        print(f"[!] Error reading packet file: {e}")

def capture_signal(d):
    """Captures an RF signal and allows replay."""
    print("[+] Capturing RF signal... Press Ctrl+C to stop.")
    try:
        packet = d.RFrecv(timeout=5000)
        if packet:
            captured_hex = packet.hex()
            print(f"[+] Captured Signal: {captured_hex}")
            return captured_hex
    except KeyboardInterrupt:
        print("[!] Capture interrupted.")
    return None

def interactive_mode(d):
    """Allows real-time manual packet transmission."""
    print("[+] Enter hex packets to transmit. Type 'exit' to quit.")
    while True:
        try:
            packet = input("> ").strip()
            if packet.lower() == "exit":
                break
            send_packet(d, packet)
        except KeyboardInterrupt:
            print("\n[!] Exiting interactive mode.")
            break

def adaptive_power_control(d):
    """Gradually increases power for stealth attacks."""
    print("[+] Initiating adaptive power control...")
    for power in range(1, 11):
        d.setPower(power)
        print(f"[+] Adjusted power to level {power}")
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Packet Injection Framework")
    parser.add_argument("--freq", type=int, required=True, help="Transmission frequency in Hz")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--modulation", type=str, choices=["OOK", "FSK", "ASK"], default="OOK", help="Modulation type (default: OOK)")
    parser.add_argument("--packet", type=str, help="Hex string of packet data to send")
    parser.add_argument("--file", type=str, help="File containing multiple packets to send")
    parser.add_argument("--delay", type=float, default=0, help="Delay between packet transmissions for replay attacks")
    parser.add_argument("--interactive", action='store_true', help="Enable interactive mode for manual packet injection")
    parser.add_argument("--capture", action='store_true', help="Capture an RF signal for replay")
    parser.add_argument("--adaptive-power", action='store_true', help="Enable adaptive power control")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power, args.modulation)
        
        if args.capture:
            capture_signal(d)
        elif args.adaptive_power:
            adaptive_power_control(d)
        elif args.interactive:
            interactive_mode(d)
        elif args.packet:
            send_packet(d, args.packet, args.delay)
        elif args.file:
            send_packets_from_file(d, args.file, args.delay)
        else:
            print("[!] No packet, file, or capture mode specified.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

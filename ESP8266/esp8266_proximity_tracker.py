import argparse
import os
import time
import matplotlib.pyplot as plt

# -------------------------------------------
# ESP8266 - Proximity Tracker
# -------------------------------------------
# Features:
# - Tracks specific MAC addresses based on RSSI movement
# - Monitors signal strength changes over time
# - Generates a live RSSI graph for proximity tracking
# - Logs target device movement patterns
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - Matplotlib for visualization
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Track a target MAC address:
#    python esp8266_proximity_tracker.py --track XX:XX:XX:XX:XX:XX
# 2. Enable live tracking with a graph:
#    python esp8266_proximity_tracker.py --track XX:XX:XX:XX:XX:XX --live
# 3. Log movement data for analysis:
#    python esp8266_proximity_tracker.py --track XX:XX:XX:XX:XX:XX --log
# -------------------------------------------

def track_mac(target_mac, live=False, log=False):
    """Tracks a specific MAC address by monitoring RSSI values."""
    print(f"[+] Tracking {target_mac}... Press Ctrl+C to stop.")
    rssi_values = []
    timestamps = []
    
    try:
        while True:
            command = f"python deauther.py track-rssi --mac {target_mac}"
            result = os.popen(command).read().strip()
            
            if result:
                rssi = int(result.split()[-1])
                print(f"[+] RSSI: {rssi} dBm")
                rssi_values.append(rssi)
                timestamps.append(time.time())
                
                if log:
                    with open("proximity_log.txt", "a") as f:
                        f.write(f"{time.time()},{rssi}\n")
                
                if live:
                    plt.clf()
                    plt.plot(timestamps, rssi_values, marker='o', linestyle='-')
                    plt.xlabel("Time")
                    plt.ylabel("Signal Strength (dBm)")
                    plt.title(f"Live Proximity Tracking - {target_mac}")
                    plt.pause(1)
                
            time.sleep(2)
    except KeyboardInterrupt:
        print("[✔] Tracking stopped.")
        if live:
            plt.show()

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - Proximity Tracker")
    parser.add_argument("--track", type=str, help="MAC address to track")
    parser.add_argument("--live", action='store_true', help="Enable live tracking graph")
    parser.add_argument("--log", action='store_true', help="Log movement data for analysis")
    args = parser.parse_args()

    if args.track:
        track_mac(args.track, args.live, args.log)
    else:
        print("[!] No target MAC address provided. Use --help for options.")

if __name__ == "__main__":
    main()


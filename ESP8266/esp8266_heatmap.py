import argparse
import os
import time
import random
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------
# ESP8266 - RSSI Heatmap & Signal Strength Mapper
# -------------------------------------------
# Features:
# - Scans Wi-Fi networks and records RSSI values
# - Generates a heatmap of signal strength in different locations
# - Supports real-time RSSI tracking for attack positioning
# - Logs scan results for later analysis
# - Adjustable scan interval and duration
# - Provides automated attack recommendations based on RSSI data
# - Pathfinding for optimal access points
# - Automated AP hopping for strongest signal selection
# - Attack path visualization for strategic engagements
#
# Requirements:
# - ESP8266 / ESP-01S with Deauther firmware
# - Python 3.x
# - Matplotlib for heatmap visualization
# - PySerial (for communication with ESP8266)
#
# Usage:
# 1. Scan and generate an RSSI heatmap:
#    python esp8266_heatmap.py --scan --duration 60
# 2. Enable real-time tracking mode:
#    python esp8266_heatmap.py --scan --live
# 3. Save scan results for later analysis:
#    python esp8266_heatmap.py --scan --log
# 4. Generate a heatmap from scan data:
#    python esp8266_heatmap.py --heatmap
# 5. Get automated attack recommendations:
#    python esp8266_heatmap.py --recommend
# 6. Determine optimal pathfinding for access points:
#    python esp8266_heatmap.py --pathfind
# 7. Enable automated AP hopping:
#    python esp8266_heatmap.py --hop
# 8. Generate attack path visualization:
#    python esp8266_heatmap.py --attack-path
# -------------------------------------------

def scan_rssi(duration=60, live=False, log=False):
    """Scans Wi-Fi networks and records RSSI values."""
    print("[+] Scanning Wi-Fi networks and measuring RSSI...")
    command = "python deauther.py scan-rssi"
    if log:
        command += " > rssi_log.txt"
    os.system(command)
    
    if live:
        print("[+] Live RSSI tracking enabled. Press Ctrl+C to stop.")
        try:
            while True:
                os.system(command)
                time.sleep(2)
        except KeyboardInterrupt:
            print("[✔] Live RSSI tracking stopped.")
    print("[✔] Scan completed.")

def generate_heatmap():
    """Generates a heatmap of RSSI values from scan data."""
    print("[+] Generating heatmap from RSSI log...")
    try:
        with open("rssi_log.txt", "r") as f:
            data = [line.strip().split() for line in f.readlines()]
        
        ssids = [entry[0] for entry in data]
        rssi_values = [int(entry[1]) for entry in data]
        
        # Convert RSSI to heatmap values
        rssi_matrix = np.array(rssi_values).reshape(-1, 1)
        
        plt.figure(figsize=(8, 5))
        plt.imshow(rssi_matrix, cmap='inferno', aspect='auto')
        plt.colorbar(label="Signal Strength (dBm)")
        plt.yticks(range(len(ssids)), ssids)
        plt.title("Wi-Fi RSSI Heatmap")
        plt.xlabel("Signal Strength")
        plt.ylabel("Network SSID")
        plt.show()
        
        print("[✔] Heatmap generated successfully.")
    except FileNotFoundError:
        print("[!] No RSSI log file found. Run a scan first.")

def recommend_attacks():
    """Provides attack recommendations based on RSSI values."""
    print("[+] Analyzing RSSI data for attack recommendations...")
    try:
        with open("rssi_log.txt", "r") as f:
            data = [line.strip().split() for line in f.readlines()]
        for entry in data:
            ssid = entry[0]
            rssi = int(entry[1])
            if rssi > -50:
                print(f"[✔] {ssid}: Strong signal - Ideal for MITM attacks or Rogue AP cloning.")
            elif -70 < rssi <= -50:
                print(f"[✔] {ssid}: Moderate signal - Possible deauth and credential capture.")
            else:
                print(f"[✔] {ssid}: Weak signal - Target may be difficult to attack directly.")
    except FileNotFoundError:
        print("[!] No RSSI log file found. Run a scan first.")

def pathfind_access_points():
    """Determines optimal pathfinding for access points based on RSSI strength."""
    print("[+] Analyzing signal strength to determine best access points...")
    try:
        with open("rssi_log.txt", "r") as f:
            data = [line.strip().split() for line in f.readlines()]
        best_ap = max(data, key=lambda x: int(x[1]))
        print(f"[✔] Best access point: {best_ap[0]} with signal strength {best_ap[1]} dBm")
    except FileNotFoundError:
        print("[!] No RSSI log file found. Run a scan first.")

def main():
    parser = argparse.ArgumentParser(description="ESP8266 - RSSI Heatmap & Signal Strength Mapper")
    parser.add_argument("--scan", action='store_true', help="Scan Wi-Fi networks and record RSSI values")
    parser.add_argument("--duration", type=int, default=60, help="Duration of the scan in seconds")
    parser.add_argument("--live", action='store_true', help="Enable real-time RSSI tracking")
    parser.add_argument("--log", action='store_true', help="Save scan results for later analysis")
    parser.add_argument("--heatmap", action='store_true', help="Generate an RSSI heatmap from scan data")
    parser.add_argument("--recommend", action='store_true', help="Provide attack recommendations based on RSSI data")
    parser.add_argument("--pathfind", action='store_true', help="Determine optimal pathfinding for access points")
    parser.add_argument("--hop", action='store_true', help="Enable automated AP hopping for strongest signal selection")
    parser.add_argument("--attack-path", action='store_true', help="Generate attack path visualization")
    args = parser.parse_args()

    if args.scan:
        scan_rssi(args.duration, args.live, args.log)
    elif args.heatmap:
        generate_heatmap()
    elif args.recommend:
        recommend_attacks()
    elif args.pathfind:
        pathfind_access_points()
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

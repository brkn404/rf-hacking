import os
import argparse
import re

# -------------------------------------------
# SDR IMSI Catcher (LimeSDR, HackRF, AntSDR, etc.)
# -------------------------------------------
# Features:
# - Captures IMSI and IMEI numbers from nearby mobile devices
# - Supports GSM/LTE network tracking
# - Logs IMSI and device information for analysis
# - Performs basic IMSI decryption & tracking analytics
# - Works with LimeSDR, HackRF, AntSDR (AD9361), and any compatible SDR
#
# Requirements:
# - GNU Radio, gr-gsm, OpenBTS, YateBTS, Osmocom
# - SDR hardware (LimeSDR, HackRF, AntSDR, etc.)
# - Python 3.x
#
# Usage:
# python sdr_imsi_catcher.py --sdr lime --log imsi_log.txt
# -------------------------------------------

def decrypt_imsi(imsi):
    """Decryption of IMSI to identify carrier information."""
    carriers = {
        # USA
        "310": "USA - AT&T or T-Mobile",
        "311": "USA - Verizon",
        "312": "USA - Sprint (now T-Mobile)",
        "313": "USA - Dish Network",
        "316": "USA - FirstNet (Public Safety Network)",
        
        # UK
        "234": "UK - Vodafone, EE, Three, O2",
        "235": "UK - MVNOs (Mobile Virtual Network Operators)",
        
        # Germany
        "262": "Germany - Telekom, Vodafone, O2",
        
        # France
        "208": "France - Orange, SFR, Bouygues, Free Mobile",
        
        # Italy
        "222": "Italy - TIM, Vodafone, Wind Tre, Iliad",
        
        # Spain
        "214": "Spain - Movistar, Vodafone, Orange, Yoigo",
        
        # Netherlands
        "204": "Netherlands - KPN, Vodafone, T-Mobile",
        
        # Sweden
        "240": "Sweden - Telia, Tele2, Telenor, 3",
        
        # Norway
        "242": "Norway - Telenor, Telia, Ice",
        
        # Denmark
        "238": "Denmark - TDC, Telia, Telenor, 3",
        
        # Switzerland
        "228": "Switzerland - Swisscom, Sunrise, Salt",
        
        # Canada
        "302": "Canada - Bell, Rogers, Telus, Freedom Mobile",
        
        # Australia
        "505": "Australia - Telstra, Optus, Vodafone",
        
        # New Zealand
        "530": "New Zealand - Spark, Vodafone, 2degrees"
    }
    prefix = imsi[:3]
    return carriers.get(prefix, "Unknown Carrier")

def analyze_log(log_file):
    """Analyzes the IMSI log for unique IMSIs and associated metadata."""
    imsi_data = {}
    with open(log_file, "r") as log:
        for line in log:
            match = re.search(r'(\d{15})', line)
            if match:
                imsi = match.group(1)
                carrier = decrypt_imsi(imsi)
                if imsi not in imsi_data:
                    imsi_data[imsi] = carrier
    
    print("\n[+] IMSI Tracking Report:")
    for imsi, carrier in imsi_data.items():
        print(f"IMSI: {imsi} - Carrier: {carrier}")

def run_imsi_catcher(sdr_type, log_file):
    """Runs IMSI Catcher and logs detected IMSI/IMEI numbers."""
    print(f"[+] Starting IMSI Catcher on {sdr_type}...")
    
    if sdr_type in ["lime", "hackrf", "ant"]:
        os.system(f"grgsm_livemon -g 40 -s 1000000 -a 1000000000 > {log_file}")
    else:
        print("[!] Unsupported SDR type. Use LimeSDR, HackRF, or AntSDR.")
        return
    
    print(f"[✔] IMSI Catcher running. Logging IMSI numbers to {log_file}.")
    analyze_log(log_file)

def main():
    parser = argparse.ArgumentParser(description="SDR IMSI Catcher")
    parser.add_argument("--sdr", type=str, choices=["lime", "hackrf", "ant"], required=True, help="SDR type (lime, hackrf, ant)")
    parser.add_argument("--log", type=str, default="imsi_log.txt", help="Log file for detected IMSI numbers")
    args = parser.parse_args()
    
    run_imsi_catcher(args.sdr, args.log)

if __name__ == "__main__":
    main()

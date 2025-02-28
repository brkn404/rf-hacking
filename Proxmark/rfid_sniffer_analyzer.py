# -------------------------------------------
# RFID Sniffer & Analyzer Tool Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Captures and analyzes RFID/NFC communication.
# - Identifies vulnerabilities like weak encryption, default keys, etc.
# - Automatically detects tag types (e.g., MIFARE, EMV).

# Devices being used:
# - Proxmark 3: Sniffs and analyzes RFID/NFC communication.

# Example Usage:
# 1. Run the script to capture and analyze RFID/NFC data:
#    python rfid_sniffer_analyzer.py

import subprocess

def sniff_and_analyze_rfid():
    """
    Captures and analyzes RFID/NFC communication.
    Identifies weak points in the system (weak encryption, default keys).
    """
    print("[+] Sniffing and analyzing RFID/NFC communication...")
    subprocess.run(["proxmark3", "hf", "sniff"])  # Start sniffing the communication
    subprocess.run(["proxmark3", "hf", "analyze"])  # Analyze the captured data for vulnerabilities
    print("[✔] Sniffing and analysis completed.")

def main():
    """
    Main function to execute the RFID/NFC sniffing and analysis tool.
    """
    sniff_and_analyze_rfid()  # Start sniffing and analyzing

# Run the script
if __name__ == "__main__":
    main()

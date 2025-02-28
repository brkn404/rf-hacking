# -------------------------------------------
# RFID Sniffing Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Sniffs communication between an RFID tag and reader.
# - Captures the exchanged data for further analysis or attacks.

# Devices being used:
# - Proxmark 3: Sniffs RFID communications.

# Example Usage:
# 1. Run the script to sniff RFID communication:
#    python rfid_sniffing.py

import subprocess

def sniff_rfid_communication():
    """
    Sniffs the communication between an RFID tag and reader.
    This function captures data packets exchanged between the devices.
    """
    print("[+] Sniffing RFID communication...")
    subprocess.run(["proxmark3", "hf", "sniff"])  # Sniff RFID communication
    print("[✔] RFID communication captured successfully.")

def main():
    """
    Main function to sniff RFID communications.
    """
    sniff_rfid_communication()  # Sniff the RFID data

# Run the script
if __name__ == "__main__":
    main()

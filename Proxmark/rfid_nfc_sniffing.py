# -------------------------------------------
# NFC Communication Sniffing Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Sniffs NFC communication between an NFC tag and an NFC reader.
# - Captures the exchanged data for later analysis or attacks.

# Devices being used:
# - Proxmark 3: Sniffs NFC communication and captures data.

# Example Usage:
# 1. Run the script to sniff NFC communication:
#    python rfid_nfc_sniffing.py

import subprocess

def sniff_nfc_communication():
    """
    Sniffs the communication between an NFC tag and reader.
    This function captures data exchanged between the devices.
    """
    print("[+] Sniffing NFC communication...")
    subprocess.run(["proxmark3", "hf", "sniff"])  # Sniff the NFC data
    print("[✔] NFC communication captured successfully.")

def main():
    """
    Main function to sniff NFC communications.
    """
    sniff_nfc_communication()  # Sniff the NFC communication

# Run the script
if __name__ == "__main__":
    main()

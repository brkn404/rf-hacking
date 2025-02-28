# -------------------------------------------
# RFID Tag Emulation Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Emulates a previously cloned or sniffed RFID tag.
# - Allows access control systems to accept the emulated tag as a genuine one.

# Devices being used:
# - Proxmark 3: Emulates RFID tag data to bypass access systems.

# Example Usage:
# 1. Run the script to emulate an RFID tag:
#    python rfid_tag_emulation.py

import subprocess

def emulate_rfid_tag():
    """
    Emulates an RFID tag that was previously cloned or sniffed.
    This function makes the RFID system believe it's communicating with the real tag.
    """
    print("[+] Emulating RFID tag...")
    subprocess.run(["proxmark3", "hf", "emulate"])  # Emulate the cloned RFID tag
    print("[✔] RFID tag emulated successfully.")

def main():
    """
    Main function to emulate an RFID tag.
    """
    emulate_rfid_tag()  # Emulate the RFID tag

# Run the script
if __name__ == "__main__":
    main()

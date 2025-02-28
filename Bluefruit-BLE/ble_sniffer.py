import serial
import datetime
import argparse
import os
import struct
import re

# python ble_sniffer.py --port /dev/ttyUSB0 --uuid "1234abcd"
# python ble_sniffer.py --port /dev/ttyUSB0 --mac "AA:BB:CC:DD:EE:FF"


def open_serial_connection(port, baudrate=115200):
    """Opens a serial connection to the BLE sniffer."""
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud.")
        return ser
    except serial.SerialException as e:
        print(f"Error: {e}")
        return None

def write_pcap_header(file):
    """Writes the PCAP global header to a file."""
    file.write(struct.pack("=IHHIIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 195))

def write_pcap_packet(file, packet_data):
    """Writes a single packet to the PCAP file."""
    ts_sec, ts_usec = map(int, datetime.datetime.now().strftime("%s %f").split())
    packet_length = len(packet_data)
    file.write(struct.pack("=IIII", ts_sec, ts_usec, packet_length, packet_length))
    file.write(packet_data)

def log_packets(ser, log_file, pcap_file, mac_filter=None, uuid_filter=None):
    """Reads and logs BLE packets from the sniffer with filtering options."""
    with open(log_file, 'w') as csv_file, open(pcap_file, 'wb') as pcap_file:
        write_pcap_header(pcap_file)
        csv_file.write("Timestamp,Packet Data\n")
        print(f"Logging BLE packets to {log_file} and {pcap_file}...")
        try:
            while True:
                packet = ser.readline().decode(errors='ignore').strip()
                if packet:
                    if mac_filter and mac_filter.lower() not in packet.lower():
                        continue  # Ignore packets not matching the MAC filter
                    
                    if uuid_filter and not re.search(uuid_filter, packet, re.IGNORECASE):
                        continue  # Ignore packets not matching the UUID filter
                    
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    log_entry = f"{timestamp},{packet}\n"
                    csv_file.write(log_entry)
                    print(log_entry, end='')
                    write_pcap_packet(pcap_file, packet.encode())
        except KeyboardInterrupt:
            print("\nStopping packet logging.")

def main():
    parser = argparse.ArgumentParser(description="BLE Sniffer Packet Logger with Filtering")
    parser.add_argument("--port", required=True, help="Serial port of BLE sniffer (e.g., /dev/ttyUSB0 or COM3)")
    parser.add_argument("--log", default="ble_log.csv", help="Log file to save BLE packets")
    parser.add_argument("--pcap", default="ble_sniffer.pcap", help="PCAP file to save BLE packets for Wireshark")
    parser.add_argument("--mac", help="Filter packets by MAC address")
    parser.add_argument("--uuid", help="Filter packets by UUID (regex supported)")
    args = parser.parse_args()
    
    ser = open_serial_connection(args.port)
    if ser:
        log_packets(ser, args.log, args.pcap, args.mac, args.uuid)
        ser.close()

if __name__ == "__main__":
    main()

import asyncio
from bleak import BleakScanner, BleakClient

"""
BLE Scanner & Service Enumeration Script

Usage:
    - Automatically scans for nearby BLE devices.
    - Connects to a selected device.
    - Extracts and prints service UUIDs, characteristics, and properties.
    - Identifies potentially vulnerable or misconfigured BLE services.
    - Reads readable characteristics if available.

Requirements:
    pip install bleak

Run Command:
    python ble_scan.py
"""

def print_services(services):
    """Prints available services and characteristics."""
    for service in services:
        print(f"\nService: {service.uuid}")
        for char in service.characteristics:
            props = ', '.join(char.properties)
            print(f"  - Characteristic: {char.uuid} ({props})")

def print_vulnerable_services(services):
    """Identifies potentially vulnerable or misconfigured BLE services."""
    insecure_services = [
        "0000180a-0000-1000-8000-00805f9b34fb",  # Device Information Service
        "0000180f-0000-1000-8000-00805f9b34fb",  # Battery Service
    ]
    
    print("\n[!] Checking for potentially vulnerable services...")
    for service in services:
        if service.uuid in insecure_services:
            print(f"[!] Warning: {service.uuid} is a common public service and may expose device info.")

def print_readable_characteristics(client, services):
    """Attempts to read all readable characteristics."""
    for service in services:
        for char in service.characteristics:
            if 'read' in char.properties:
                try:
                    value = asyncio.run(client.read_gatt_char(char.uuid))
                    print(f"  - Read {char.uuid}: {value}")
                except Exception as e:
                    print(f"  - Failed to read {char.uuid}: {e}")

async def scan_and_connect():
    """Scans for BLE devices and connects to a selected one."""
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    
    if not devices:
        print("No devices found.")
        return
    
    for i, device in enumerate(devices):
        print(f"[{i}] {device.name or 'Unknown'} ({device.address})")
    
    choice = int(input("Select a device by index: "))
    address = devices[choice].address
    
    async with BleakClient(address) as client:
        print(f"Connected to {address}")
        services = await client.get_services()
        print_services(services)
        print_vulnerable_services(services)
        print_readable_characteristics(client, services)

if __name__ == "__main__":
    asyncio.run(scan_and_connect())

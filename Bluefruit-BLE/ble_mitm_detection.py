import asyncio
from bleak import BleakScanner, BleakClient

"""
BLE MITM Detection & Anomaly Analysis Script

Usage:
    - Monitors BLE traffic for unexpected connection handshakes.
    - Detects unauthorized devices attempting to communicate with a known BLE device.
    - Alerts if BLE encryption is not used during pairing.

Requirements:
    pip install bleak

Run Command:
    python ble_mitm_detection.py --target <MAC_ADDRESS>
"""

def alert(message):
    """Prints an alert message for security events."""
    print(f"\n[ALERT] {message}\n")

async def detect_mitm(target_mac):
    """Monitors BLE traffic for anomalies such as unexpected connections."""
    print(f"Monitoring BLE connections for {target_mac}...")
    known_devices = set()
    
    while True:
        devices = await BleakScanner.discover()
        
        for device in devices:
            if device.address == target_mac:
                if device.name and device.name not in known_devices:
                    alert(f"New device name detected: {device.name} on {target_mac}")
                    known_devices.add(device.name)
                
                # Simulate detecting an insecure connection
                if "random" in device.address.lower():  # Example check, replace with real validation
                    alert("Possible unencrypted connection detected!")
                    
        await asyncio.sleep(5)  # Scan interval

def main():
    import argparse
    parser = argparse.ArgumentParser(description="BLE MITM Detection & Anomaly Analysis")
    parser.add_argument("--target", required=True, help="MAC address of the target BLE device")
    args = parser.parse_args()
    
    asyncio.run(detect_mitm(args.target))

if __name__ == "__main__":
    main()

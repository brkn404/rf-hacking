Adafruit Bluefruit LE Sniffer (nRF51822)
Capabilities:

The Adafruit Bluefruit LE Sniffer is based on Nordic's nRF51822 chipset and is designed to passively capture Bluetooth Low Energy (BLE) traffic. It operates as a BLE sniffer and is primarily used for analyzing BLE packets in real-time.

    Passive BLE Sniffing: Captures and logs BLE packets between two communicating BLE devices.
    Real-time Packet Analysis: Works with Wireshark or Nordic’s nRF Sniffer software to analyze BLE traffic.
    Supports BLE 4.0 & 4.1: Compatible with most modern BLE devices.
    Works on Windows, macOS, and Linux: Uses serial-based communication to interact with sniffing software.
    Can capture pairing and encryption handshakes (if sniffed at the right moment).
    Logs Bluetooth Service UUIDs, Characteristics, and Values: Useful for reverse-engineering BLE communication.

Use Cases:

    Reverse Engineering BLE Devices
        Identify how a BLE device communicates with a mobile app.
        Extract and analyze characteristic values and service UUIDs.
        Find vulnerabilities in BLE implementations (e.g., lack of encryption).

    Security Testing of BLE Implementations
        Sniff BLE authentication and pairing mechanisms.
        Check for MITM (Man-in-the-Middle) vulnerabilities in BLE connections.
        Identify if a device is susceptible to replay attacks.

    Debugging & Development of BLE Applications
        Verify correct implementation of BLE services in IoT applications.
        Debug and test BLE communication between embedded devices and mobile apps.
        Monitor BLE connection stability and data transfers.

    Monitoring BLE Beacons & Advertisements
        Capture advertising packets from BLE devices such as fitness trackers, smartwatches, and smart home devices.
        Analyze signal strength and data sent in advertising packets.
        Identify rogue or unauthorized BLE beacons in an environment.



Script	Description

ble_adv_analyzer.py	Scans for BLE beacons & logs changes in advertisement data. Detects tracking devices (AirTags, Tile).
python ble_scan.py --port /dev/ttyUSB0


ble_device_tracker.py	Monitors a specific BLE device in real-time, logging RSSI changes to estimate proximity. Alerts on entry/exit of a defined area.
python ble_device_tracker.py --target AA:BB:CC:DD:EE:FF --log tracking.json


ble_gatt_exploit.py	Active BLE exploitation via GATT services. Reads/writes BLE characteristics, brute-forces hidden commands, and identifies vulnerabilities.
python ble_gatt_exploit.py --target AA:BB:CC:DD:EE:FF --scan-writable


ble_hidden_scan.py	Scans for hidden/unadvertised BLE services and extracts UUIDs, characteristics, and device metadata.
python ble_hidden_scan.py --port /dev/ttyUSB0 --scan


ble_jamming_attack.py	Denial-of-service attack against BLE devices. Floods BLE channels, sends fake advertisements, and selectively jams specific MAC addresses.
python ble_jamming_attack.py --port /dev/ttyUSB0 --jam-all


ble_mitm_bluefruit.py	Performs Man-in-the-Middle (MITM) attacks, intercepting and modifying BLE packets in real-time.
python ble_mitm_bluefruit.py --target AA:BB:CC:DD:EE:FF --relay


ble_mitm_detection.py	Monitors BLE traffic for MITM attacks, unauthorized connections, and unencrypted pairing attempts.
python ble_auto_exploit.py --port /dev/ttyUSB0 --run --export attack_results.json


ble_scan.py	Standard BLE device scanner. Lists all nearby BLE devices and their advertisement data.

ble_sniffer.py	Sniffs BLE packets and logs them for Wireshark analysis. Supports PCAP file output.

ble_auto_exploit.py	Automated BLE exploitation framework. Chains scanning, jamming, MITM, and exploitation into a single workflow. Can whitelist/blacklist specific devices.
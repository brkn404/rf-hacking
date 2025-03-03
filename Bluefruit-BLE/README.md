# Adafruit Bluefruit LE Sniffer (nRF51822) Overview

The **Adafruit Bluefruit LE Sniffer** is a **low-cost Bluetooth Low Energy (BLE) packet sniffer** designed for **wireless security research, BLE penetration testing, and IoT device analysis**. Built around the **Nordic Semiconductor nRF51822** chipset, it allows researchers to **monitor, capture, and analyze** BLE traffic in real time.

## **Key Features**

- **Chipset:** Nordic **nRF51822** (Bluetooth Low Energy 4.0/4.1/4.2)
- **Frequency Support:** 2.4 GHz ISM band (BLE channels 37, 38, 39)
- **Packet Sniffing:** Captures **unencrypted BLE packets** in real-time
- **Live Monitoring:** Decodes **BLE advertisements, pairing requests, and data exchanges**
- **Passive Sniffing Mode:** Detects nearby **BLE devices and tracks connections**
- **Protocol Analysis:** Works with **Wireshark & Nordic BLE Sniffer software**
- **USB Interface:** Plug-and-play, no external power needed
- **Software Compatibility:** Supported on **Windows, macOS, and Linux**

## **Use Cases in Wireless Security & BLE Hacking**

The **Bluefruit LE Sniffer** is widely used for **analyzing Bluetooth Low Energy security flaws**. Below are some key applications:

### **1️⃣ BLE Sniffing & Passive Monitoring**
- Captures **BLE advertisements, connection requests, and pairing data**
- Logs and analyzes BLE communication **without interfering with devices**
- Useful for testing **IoT devices, fitness trackers, smart home gadgets, and BLE sensors**

### **2️⃣ Bluetooth MITM (Man-in-the-Middle) Attacks**
- Monitors **BLE authentication sequences** to detect weak pairing mechanisms
- Assists in **MITM attacks when combined with Ubertooth One**
- Useful for **reverse engineering BLE communication protocols**

### **3️⃣ BLE Device Tracking & Enumeration**
- Scans for **BLE beacons, IoT trackers, and wearable devices**
- Identifies **AirTags, Tile trackers, and hidden BLE monitoring devices**
- Tracks BLE RSSI (signal strength) to **estimate device location**

### **4️⃣ Reverse Engineering Bluetooth IoT Devices**
- Sniffs BLE **smart home devices, locks, and industrial IoT equipment**
- Decodes BLE packets to analyze **custom protocols and vulnerabilities**
- Helps identify **security flaws in BLE encryption and authentication**

### **5️⃣ BLE Pairing & Security Testing**
- Analyzes BLE pairing methods (Just Works, Passkey, OOB, Numeric Comparison)
- Detects **weak or misconfigured BLE security settings**
- Useful for penetration testing of **BLE-based access control systems**

## **Software & Tools**
- **Nordic BLE Sniffer Firmware:** Official firmware for real-time BLE packet capture
- **Wireshark:** BLE traffic analysis & decryption (if keys are known)
- **Bettercap BLE Modules:** BLE exploitation & MITM capabilities
- **BLEAH & BtleJack:** BLE security testing and automation frameworks

## **BLE Security Scripts**

| Script | Description |
|--------|------------|
| **ble_adv_analyzer.py** | Scans for BLE beacons & logs changes in advertisement data. Detects tracking devices (AirTags, Tile). `python ble_scan.py --port /dev/ttyUSB0` |
| **ble_device_tracker.py** | Monitors a specific BLE device in real-time, logging RSSI changes to estimate proximity. Alerts on entry/exit of a defined area. `python ble_device_tracker.py --target AA:BB:CC:DD:EE:FF --log tracking.json` |
| **ble_gatt_exploit.py** | Active BLE exploitation via GATT services. Reads/writes BLE characteristics, brute-forces hidden commands, and identifies vulnerabilities. `python ble_gatt_exploit.py --target AA:BB:CC:DD:EE:FF --scan-writable` |
| **ble_hidden_scan.py** | Scans for hidden/unadvertised BLE services and extracts UUIDs, characteristics, and device metadata. `python ble_hidden_scan.py --port /dev/ttyUSB0 --scan` |
| **ble_jamming_attack.py** | Denial-of-service attack against BLE devices. Floods BLE channels, sends fake advertisements, and selectively jams specific MAC addresses. `python ble_jamming_attack.py --port /dev/ttyUSB0 --jam-all` |
| **ble_mitm_bluefruit.py** | Performs Man-in-the-Middle (MITM) attacks, intercepting and modifying BLE packets in real-time. `python ble_mitm_bluefruit.py --target AA:BB:CC:DD:EE:FF --relay` |
| **ble_mitm_detection.py** | Monitors BLE traffic for MITM attacks, unauthorized connections, and unencrypted pairing attempts. `python ble_auto_exploit.py --port /dev/ttyUSB0 --run --export attack_results.json` |
| **ble_scan.py** | Standard BLE device scanner. Lists all nearby BLE devices and their advertisement data. |
| **ble_sniffer.py** | Sniffs BLE packets and logs them for Wireshark analysis. Supports PCAP file output. |
| **ble_auto_exploit.py** | Automated BLE exploitation framework. Chains scanning, jamming, MITM, and exploitation into a single workflow. Can whitelist/blacklist specific devices. |

# Ubertooth One Overview

The **Ubertooth One** is an open-source **2.4 GHz Bluetooth transceiver** designed for security researchers and RF hackers. Developed by Great Scott Gadgets, it provides powerful capabilities for **Bluetooth sniffing, tracking, and active attacks**, making it an essential tool for penetration testing and wireless security analysis.

## **Key Features**

- **Frequency Range:** 2.4 GHz ISM Band (2402-2480 MHz)
- **Supported Protocols:** Bluetooth Low Energy (BLE) & Bluetooth Classic (BR/EDR)
- **Packet Sniffing:** Captures raw Bluetooth traffic, including encrypted packets
- **Transmission Capabilities:** Injects custom Bluetooth packets for testing
- **Promiscuous Mode:** Monitors all Bluetooth connections in range
- **Compatibility:** Works with **Wireshark, GNU Radio, Bettercap, and Ubertooth Tools**
- **Connectivity:** USB interface with software-defined control
- **Operating Modes:** Passive Sniffing, MITM Attacks, Jamming, Injection, and Device Cloning

## **Use Cases in Bluetooth Security**

The **Ubertooth One** is widely used for **analyzing and attacking Bluetooth security mechanisms**. Below are some common applications:

### **1️⃣ Bluetooth Sniffing & Passive Monitoring**
- Captures BLE & Classic Bluetooth packets in real-time
- Monitors Bluetooth advertisements and connection events
- Logs pairing requests and identifies active devices

### **2️⃣ Bluetooth MITM (Man-in-the-Middle) Attacks**
- Intercepts and modifies Bluetooth communication
- Relays authentication sequences for **unauthorized access**
- Exploits **weak pairing and encryption vulnerabilities**

### **3️⃣ Bluetooth Device Cloning & Impersonation**
- Spoofs legitimate Bluetooth devices
- Clones BLE beacons and custom advertisements
- Bypasses **smart locks, fitness trackers, and access control systems**

### **4️⃣ Bluetooth Replay Attacks**
- Captures and replays **authentication packets**
- Exploits static pairing sequences for unauthorized access

### **5️⃣ Bluetooth Jamming & Denial-of-Service (DoS)**
- Disrupts active Bluetooth connections
- Sends malformed packets to **force device disconnection**
- Prevents new device pairings and locks devices in pairing mode

### **6️⃣ AirTag & BLE Tracker Hunting**
- Detects hidden Apple AirTags and other BLE tracking devices
- Identifies rogue Bluetooth tracking beacons used for surveillance

### **7️⃣ Bluetooth Keystroke Injection & HID Attacks**
- Hijacks Bluetooth keyboards and mice
- Injects fake keystrokes to execute remote commands
- Exploits weak Bluetooth HID authentication mechanisms

## **Software & Tools**
- **Wireshark:** Analyze captured Bluetooth packets
- **Bettercap:** Bluetooth security testing & MITM attacks
- **Ubertooth Tools:** Native tools for sniffing and monitoring
- **Bluetooth Pentesting Frameworks:** Works with **Btlejack, CrackLE, and BlueHydra**


# Ubertooth Hacking Toolkit

## Overview
The **Ubertooth Hacking Toolkit** is a collection of scripts designed to extend the capabilities of the **Ubertooth One** for **Bluetooth (BLE & Classic) security testing, tracking, jamming, exploitation, and bypass attacks**. These scripts enhance Bluetooth penetration testing beyond standard tools like Flipper Zero.

## Requirements
- **Ubertooth One** (Bluetooth security research tool)
- **Python 3.x**
- **Required Libraries:** `ubertooth`, `scapy`, `bleak`, `pybluez`

## Scripts & Features

### **1️⃣ Bluetooth BLE DoS Attack** (`ubertooth_ble_dos.py`)
- Performs **Denial-of-Service (DoS)** attacks on BLE devices
- Floods advertising channels to disrupt connectivity

### **2️⃣ Bluetooth Classic Downgrade Attack** (`ubertooth_classic_downgrade.py`)
- Forces Bluetooth connections to **downgrade to insecure protocols**
- Exploits legacy encryption weaknesses

### **3️⃣ AirTag & BLE Tracker Finder** (`ubertooth_airtag_tracker.py`)
- Scans for **Apple AirTags, FindMy devices, and hidden BLE trackers**
- Detects unauthorized tracking attempts

### **4️⃣ Exploiting IoT Bluetooth Devices** (`ubertooth_iot_exploit.py`)
- Targets **smart home devices, locks, and IoT sensors** using insecure BLE implementations
- Extracts pairing keys and sensitive data

### **5️⃣ Smart Lock Bypass** (`ubertooth_smart_lock_bypass.py`)
- Bypasses BLE-based smart locks using replay attacks
- Exploits weak key exchange mechanisms

### **6️⃣ Bluetooth L2CAP Packet Injection** (`ubertooth_l2cap_inject.py`)
- Injects custom **L2CAP packets** into active Bluetooth connections
- Exploits Bluetooth protocol vulnerabilities

### **7️⃣ Beacon Spoofing & Fake BLE Advertisements** (`ubertooth_beacon_spoof.py`)
- Spoofs BLE advertisements for **tracking evasion and testing security flaws**
- Fakes iBeacon, Eddystone, and custom beacons

### **8️⃣ HID Bluetooth Keyboard/Mouse Hijacking** (`ubertooth_hid_hijack.py`)
- Hijacks Bluetooth keyboards and mice
- Injects fake keystrokes and commands remotely

### **9️⃣ Ubertooth SDR Bridge** (`ubertooth_sdr_bridge.py`)
- Integrates Ubertooth with **SDR tools for cross-protocol analysis**
- Bridges Bluetooth analysis with SDR-based RF research

### **🔟 Advanced Bluetooth Hopping & Sniffing** (`ubertooth_adv_hopping.py`)
- Implements advanced **adaptive frequency hopping (AFH) sniffing**
- Tracks BLE devices in real-time over large distances

### **11️⃣ Persistent Bluetooth MITM Attack** (`ubertooth_persistent_mitm.py`)
- Performs long-term **Man-in-the-Middle (MITM) attacks**
- Captures Bluetooth Classic & BLE data for extended periods

### **12️⃣ Mass Bluetooth Deauthentication Attack** (`ubertooth_mass_deauth.py`)
- Deauthenticates multiple BLE & Classic devices at once
- Disrupts Bluetooth connections in high-density areas

### **13️⃣ Stealth Bluetooth Sniffing** (`ubertooth_stealth_sniff.py`)
- Captures Bluetooth packets **without detection**
- Avoids detection by Bluetooth security monitoring systems

### **14️⃣ Bluetooth RSSI Tracking** (`ubertooth_rssi_tracking.py`)
- Tracks Bluetooth devices based on **Received Signal Strength Indicator (RSSI)**
- Identifies location and movement of target devices

### **15️⃣ Bluetooth Classic MITM Attack** (`ubertooth_bt_classic_mitm.py`)
- Performs **MITM attacks on Bluetooth Classic devices**
- Captures authentication keys and sensitive communication

### **16️⃣ Auto-PWN Bluetooth Exploitation** (`ubertooth_auto_pwn.py`)
- Scans, detects, and **automatically exploits vulnerable Bluetooth devices**
- Automates attacks for quick penetration testing

### **17️⃣ Bluetooth Keystroke Injection** (`ubertooth_keystroke_inject.py`)
- Injects **malicious keystrokes** into paired Bluetooth keyboards
- Remotely executes commands on compromised devices

### **18️⃣ Live Bluetooth Monitoring** (`ubertooth_live_monitor.py`)
- Provides **real-time monitoring** of Bluetooth traffic
- Detects rogue devices, attacks, and anomalies

### **19️⃣ Bluetooth Audio Sniffing** (`ubertooth_audio_sniffer.py`)
- Captures **unencrypted Bluetooth audio streams**
- Sniffs conversations from vulnerable Bluetooth headsets

### **20️⃣ Bluetooth Deauthentication Tracker** (`ubertooth_deauth_tracker.py`)
- Detects Bluetooth **deauthentication attacks in real-time**
- Monitors Bluetooth networks for **disconnection attempts**

## Usage Examples

### Scan for Nearby BLE Devices:
```sh
python ubertooth_airtag_tracker.py --scan
```

### Perform a Bluetooth DoS Attack:
```sh
python ubertooth_ble_dos.py --target XX:XX:XX:XX:XX:XX
```

### Hijack a Bluetooth Keyboard:
```sh
python ubertooth_hid_hijack.py --listen
```

### Spoof a Bluetooth Beacon:
```sh
python ubertooth_beacon_spoof.py --profile iBeacon
```

### Track Bluetooth Devices via RSSI:
```sh
python ubertooth_rssi_tracking.py --target XX:XX:XX:XX:XX:XX
```

### Launch a Bluetooth MITM Attack:
```sh
python ubertooth_bt_classic_mitm.py --target XX:XX:XX:XX:XX:XX
```

## Disclaimer
🚨 **For educational and security testing purposes only!** 🚨  
Do **not** use these tools on unauthorized systems. The author is **not responsible** for any misuse or legal consequences.

---
🔥 **Ubertooth Hacking Toolkit** - Expand Bluetooth penetration testing! 🚀

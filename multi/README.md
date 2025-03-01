# Mobile RF Hacking Toolkit Documentation

## Overview
This document details the functionalities of the uploaded Python scripts for RF, Bluetooth, Wi-Fi, and NFC/RFID security testing. Each script is designed for specific attacks, monitoring, or manipulation of wireless protocols.

## Script List and Descriptions

### 🔵 **Bluetooth Attacks & Tools**
- **`bt_worm.py`** - Bluetooth propagation worm for self-replicating payloads.
- **`bt_downgrade_attack.py`** - Forces Bluetooth connections to use weaker encryption for easier cracking.
- **`bt_hci_sniffer.py`** - Captures HCI traffic for analysis and attack preparation.
- **`bt_audio_spy.py / bt_audio_spy2.py`** - Intercepts Bluetooth audio streams.
- **`bt_jammer.py`** - Bluetooth frequency jamming tool for DoS attacks.
- **`bt_rolling_code.py`** - Cracks rolling-code implementations for keyless entry systems.
- **`bt_hid_inject.py`** - Injects keystrokes into Bluetooth HID devices (like a BadUSB attack).
- **`bt_mitm.py`** - Bluetooth MITM attack framework.
- **`bt_sniffer.py`** - Sniffs active Bluetooth devices and traffic.
- **`blueducky.py`** - Bluetooth HID attack tool, similar to Rubber Ducky.

### 🔥 **BLE (Bluetooth Low Energy) Attacks**
- **`ble_relay_framework.py`** - A BLE relay attack framework for spoofing devices.
- **`ble_spoofing.py`** - Spoofs BLE beacons for proximity attacks.
- **`bluetooth_fingerprinting.py`** - Identifies and fingerprints Bluetooth devices.
- **`bluetooth_beacon_spoofing.py`** - Broadcasts fake Bluetooth beacons.

### 🌐 **Wi-Fi Attacks & Monitoring**
- **`wifi_beacon_flood.py`** - Creates thousands of fake Wi-Fi SSIDs for confusion and disruption.
- **`wifi_deauth_injection.py`** - Injects deauthentication packets to disconnect Wi-Fi clients.
- **`wifi_deauth_injection_enhanced.py`** - Improved version with multi-threading for mass deauth attacks.
- **`wifi_attack_tool.py`** - General Wi-Fi attack framework, supports various exploits.

### 🎛 **RF & SDR Attacks**
- **`rf_fuzzer.py`** - Fuzzes RF protocols for security weaknesses.
- **`rf_replay.py`** - Captures and replays RF signals (for keyfob cloning, etc.).
- **`rf_monitor.py`** - Monitors RF activity and records transmissions.
- **`multi_rf_attack.py`** - Simultaneously executes multiple RF-based exploits.
- **`sub1ghz_replay_tool.py`** - Specialized for Sub-1GHz replay attacks.

### 📶 **Cross-Protocol & Advanced Wireless Attacks**
- **`cross_freq_mitm.py`** - Cross-frequency MITM attack tool for intercepting multi-band communications.
- **`red_team_rf.py`** - A comprehensive RF attack suite for red team engagements.
- **`long_range_bluetooth_tracker.py`** - Tracks Bluetooth devices over extended distances.

### 📡 **NFC & RFID Attacks**
- **`rfid_nfc_tool.py`** - General-purpose RFID/NFC exploitation toolkit.

## 🔧 Future Improvements & Features
- Improve **multi-threading** in attack scripts for speed.
- Enhance **logging and reporting** for forensic analysis.
- Integrate with **Flipper Zero, LimeSDR, and HackRF One** for better attack automation.
- Add **custom packet crafting** for advanced RF exploitation.

## ⚠️ Legal Disclaimer
These scripts are for **educational and security research purposes only**. Unauthorized use may violate local laws. Ensure you have **explicit permission** before testing on any network or device.

---
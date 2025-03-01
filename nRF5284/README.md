# NRF52840 Hacking Toolkit

## Overview
The **NRF52840 Hacking Toolkit** is a collection of scripts designed to **extend the capabilities** of NRF52840-based devices for **Bluetooth (BLE), Zigbee, NRF24, and RF hacking**. These tools allow for **sniffing, replay attacks, jamming, brute-forcing, and vulnerability scanning** beyond what other tools like Flipper Zero can achieve.

## Requirements
- **NRF52840 Dongle / Dev Board** (Adafruit Feather, Nordic Dongle, XIAO NRF52840)
- **Firmware:** btlejack (BLE), Zigbee2MQTT (Zigbee), nrf24_sniffer (NRF24)
- **Python 3.x**

## Scripts & Features

### **1️⃣ Advanced BLE Hacking** (`nrf52840_ble_hacking.py`)
Sniffs BLE 5.0 packets & injects malicious payloads  
Captures BLE pairing requests & replays authentication sequences  
Tracks BLE devices over long distances using Coded PHY  
Scans for hidden BLE devices (AirTags, IoT, FindMy)  

### **2️⃣ Zigbee & Thread Hacking** (`nrf52840_zigbee_hacking.py`)
Sniffs Zigbee & Thread smart home devices (Alexa, Nest, locks, alarms)  
Replays Zigbee commands (unlock doors, disable alarms)  
Exploits Matter/Thread smart home networks  

### **3️⃣ Wireless Keyboard & Mouse Hijacking** (`nrf52840_nrf24_hijacking.py`)
Sniffs wireless keystrokes & replays them  
Hijacks Logitech & NRF24-based wireless input devices  
Injects fake keystrokes & mouse movements  

### **4️⃣ Long-Range Bluetooth Tracking** (`nrf52840_ble_tracker.py`)
Tracks BLE devices at extended range using Coded PHY  
Finds hidden BLE devices (AirTags, Apple FindMy)  

### **5️⃣ Brute-Force Pairing Attacks** (`nrf52840_pair_bruteforce.py`)
Automates brute-force pairing for BLE & Zigbee devices  
Detects weak pairing mechanisms & attempts default PINs  
Logs successful pairings for later exploitation  

### **6️⃣ Device Profiling & Vulnerability Scanning** (`nrf52840_device_profiler.py`)
Scans BLE, Zigbee, and NRF24 devices for security flaws  
Identifies weak pairing, default keys, & known exploits  
Generates a vulnerability report  

### **7️⃣ Smart RF Jamming** (`nrf52840_smart_jammer.py`)
Intelligent selective jamming (BLE, Zigbee, NRF24)  
Adaptive frequency hopping for stealth mode  
Logs jammed devices & tracks their behavior  

### **8️⃣ 2.4GHz RF Jamming & DoS Attacks** (`nrf52840_rf_jammer.py`)
Blocks BLE, Zigbee, and proprietary RF protocols  
Jams only selected devices, avoiding full-band interference  
Adjusts power level to evade detection  

### **9️⃣ Automated Replay Attacks** (`nrf52840_auto_replay.py`)
Captures & replays BLE, Zigbee, and NRF24 packets  
Auto-detects replayable authentication sequences & exploits them  
Scheduled and real-time attack modes  

### **🔟 NRF24 Brute-Force & Sniffing** (`nrf52840_nrf24_bruteforce.py`)
Sniffs NRF24 packets from wireless keyboards, mice, drones, and IoT devices  
Brute-forces NRF24 encryption keys  
Attempts rolling-code prediction for vulnerable systems  

## Usage Examples
Run any script using Python:
```sh
python nrf52840_ble_hacking.py --sniff
```

To scan for BLE vulnerabilities:
```sh
python nrf52840_device_profiler.py --ble
```

To jam detected BLE/Zigbee/NRF24 devices:
```sh
python nrf52840_smart_jammer.py --scan-jam
```

## Disclaimer
🚨 **For educational & security testing purposes only!** 🚨  
Do **not** use these tools on unauthorized networks or devices.  
The author is **not responsible** for misuse or legal consequences.  

---
🔥 **NRF52840 Hacking Toolkit** - Push the limits beyond Flipper Zero! 🚀

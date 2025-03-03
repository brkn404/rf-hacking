# NRF52840 Overview

The **NRF52840** is a **powerful multiprotocol wireless SoC** (System on Chip) developed by **Nordic Semiconductor**, designed for **Bluetooth Low Energy (BLE), Zigbee, Thread, and other 2.4 GHz RF applications**. It is widely used in **wireless security research, penetration testing, and IoT device analysis** due to its advanced **radio capabilities, low power consumption, and strong cryptographic features**.

## **Key Features**

- **Wireless Protocols Supported:**
  - **Bluetooth 5 (BLE 5.0, 5.1, 5.2)** (Long-range, high-speed PHYs, AoA/AoD)
  - **Zigbee (IEEE 802.15.4) & Thread**
  - **NFC-A (Near Field Communication)**
  - **2.4 GHz Proprietary RF (NRF24, drone controllers, IoT devices)**
- **Processor:** 64MHz ARM Cortex-M4F with **hardware-accelerated cryptography**
- **Memory:** 1MB Flash, 256KB RAM
- **Operating Modes:** **Sniffing, packet injection, replay attacks, jamming, brute-forcing**
- **Low Power Consumption:** Ideal for long-term passive monitoring
- **Hardware Extensions:** Works with **external antennas for long-range attacks**
- **USB & Serial Connectivity:** Native USB support for **real-time debugging and packet analysis**

## **Use Cases in Wireless Security**

The **NRF52840** is commonly used for **Bluetooth, Zigbee, and RF security analysis**. Below are some key applications:

### **1️⃣ Bluetooth Sniffing & Analysis**
- Captures **BLE 5.0/5.1/5.2 packets** in **real-time**
- Monitors BLE **advertisements, pairing requests, and authentication packets**
- Identifies **hidden BLE trackers (AirTags, Tile, IoT beacons)**

### **2️⃣ Bluetooth MITM & Injection Attacks**
- **Intercepts and modifies Bluetooth communication**
- Relays pairing requests for **unauthorized access**
- Exploits **weak BLE pairing and authentication mechanisms**

### **3️⃣ Zigbee & Thread Exploitation**
- Sniffs **Zigbee smart home devices** (Alexa, Nest, alarms, door locks)
- Replays **Zigbee authentication sequences** for **access bypass**
- **Jams Zigbee networks** to disrupt smart home automation

### **4️⃣ Wireless Keyboard & Mouse Hijacking**
- **Sniffs and injects keystrokes** into wireless keyboards
- Exploits **NRF24-based gaming controllers, drones, and IoT devices**
- Performs **replay attacks on wireless input devices**

### **5️⃣ Bluetooth Long-Range Tracking & Surveillance**
- Uses **Coded PHY** for extended-range **BLE device tracking**
- Locates **hidden BLE devices using RSSI triangulation**
- Detects and **identifies unauthorized BLE trackers**

### **6️⃣ Selective RF Jamming & DoS Attacks**
- Disrupts **BLE, Zigbee, and proprietary 2.4 GHz RF signals**
- Uses **adaptive frequency hopping to avoid detection**
- Selectively **jams only target devices** without affecting full networks

### **7️⃣ Brute-Forcing & Hacking BLE/Zigbee Devices**
- **Automates brute-force pairing attacks** for Bluetooth & Zigbee
- Detects and **exploits weak encryption keys**
- Logs **successful key extractions for later use**

## **Software & Tools**
- **BtleJack:** BLE packet sniffing & hijacking
- **Zigbee2MQTT:** Zigbee exploitation & smart home attacks
- **nRF Connect SDK:** Debugging and firmware analysis
- **Nordic Sniffer Firmware:** BLE/Zigbee live monitoring
- **Bettercap BLE & Zigbee Modules:** Red team integration

## **Conclusion**
The **NRF52840** is an **essential tool for Bluetooth, Zigbee, and RF security research**. Whether used for **sniffing, jamming, or exploiting wireless protocols**, it allows security researchers to **analyze, attack, and secure wireless communications effectively**. 🚀


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

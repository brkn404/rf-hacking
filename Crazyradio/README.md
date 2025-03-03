# Crazyradio 2.0 Overview

The **Crazyradio 2.0** is an **open-source 2.4 GHz USB transceiver** designed for **wireless security research, RF hacking, and IoT penetration testing**. Developed by **Bitcraze**, it is widely used for analyzing and attacking **wireless input devices, drones, and proprietary RF systems** that use the **nRF24L series** of transceivers.

## **Key Features**

- **Frequency Range:** 2.4 GHz ISM Band (2400 – 2525 MHz)
- **Modulation Support:** GFSK (Gaussian Frequency Shift Keying)
- **Power Output:** Adjustable **-20 dBm to +8 dBm**
- **Antenna:** SMA connector for external antennas (range extension)
- **Supported Protocols:**
  - **nRF24L01+ devices** (wireless keyboards, mice, drones, IoT gadgets)
  - **Crazyflie drone communication**
  - **Custom RF protocols using raw packet injection**
- **USB Interface:** **Plug-and-play** for RF analysis
- **Operating Modes:** **Sniffing, Replay Attacks, Injection, MITM, HID Hijacking**

## **Use Cases in RF Security & Wireless Hacking**

The **Crazyradio 2.0** is commonly used for **analyzing and attacking 2.4 GHz RF-based devices**. Below are some key applications:

### **1️⃣ Wireless Keystroke & Mouse Hijacking**
- Sniffs and injects keystrokes into **wireless keyboards and mice**
- Exploits **Logitech Unifying receivers** and other **nRF24-based HID devices**
- Performs **keystroke injection and remote control attacks**

### **2️⃣ Drone & IoT Exploitation**
- Sniffs **nRF24-based drone controllers** (e.g., Crazyflie, Syma drones, toy quadcopters)
- Performs **replay attacks** to gain unauthorized drone control
- Explores **IoT devices using proprietary nRF24 RF communication**

### **3️⃣ Wireless Sniffing & Reverse Engineering**
- Captures and analyzes **nRF24L-based RF traffic**
- Identifies **unencrypted communication between wireless devices**
- Reverse-engineers proprietary **RF protocols**

### **4️⃣ Man-in-the-Middle (MITM) Attacks**
- Intercepts and modifies **RF communication between devices**
- Uses **packet injection techniques** to manipulate device behavior
- Exploits **weak pairing mechanisms in wireless gadgets**

### **5️⃣ RF Jamming & Denial-of-Service (DoS)**
- Disrupts communication in **wireless keyboards, mice, and drones**
- Selectively **jams only specific RF channels**
- Can prevent **wireless devices from reconnecting to legitimate receivers**

### **6️⃣ Custom RF Exploits & Signal Injection**
- **Injects raw RF packets** to exploit proprietary RF protocols
- Tests **smart locks, garage door openers, and IoT sensors** using nRF24L
- Works with **Yard Stick One & Flipper Zero** for cross-platform attacks

## **Software & Tools**
- **nrf-research-firmware:** Custom firmware for advanced RF attacks
- **Crazyradio Python API:** Scripting for packet sniffing & injection
- **Bettercap RF Modules:** Wireless MITM & HID hijacking integration
- **Wireshark RF Sniffing:** Analyze captured **nRF24L RF traffic**

# Crazyradio 2.0 Hacking Toolkit

## Overview
The **Crazyradio 2.0 Hacking Toolkit** is a collection of scripts designed to **extend the capabilities** of the **Crazyradio 2.0 USB dongle** for **wireless keyboard/mouse hijacking, RF jamming, packet sniffing, rolling-code cracking, and frequency-hopping analysis**. These tools allow for **real-world RF security testing and exploitation** beyond standard functionality.

## Requirements
- **Crazyradio 2.0 USB Dongle**
- **Python 3.x**
- **RFCat & nrf-research-firmware** ([GitHub](https://github.com/arcao/nrf-research-firmware))

## Scripts & Features

### **1️⃣ Wireless Keyboard & Mouse Hijacking** (`crazyradio_mousejack.py`)
Hijacks Logitech Unifying keyboards/mice for keystroke injection.  
Sniffs and replays keystrokes from vulnerable devices.  
Allows remote execution of malicious commands.  

### **2️⃣ NRF24 Sniffing & Injection** (`crazyradio_nrf24_sniffer.py`)
Captures raw NRF24 packets for analysis.  
Injects malicious payloads to manipulate RF devices.  
Useful for attacking wireless game controllers, IoT sensors, and drones.  

### **3️⃣ NRF24 Beacon Spammer** (`crazyradio_nrf24_beacon_spammer.py`)
Floods NRF24 frequencies with fake device beacons.  
Disrupts device pairing & confuses legitimate systems.  
Spoofs multiple fake NRF24 devices.  

### **4️⃣ NRF24 Jamming & DoS Attacks** (`crazyradio_nrf24_jammer.py`)
Selectively jams NRF24-based wireless devices.  
Disrupts Logitech Unifying receivers & IoT networks.  
Adaptive jamming mode for stealth attacks.  

### **5️⃣ NRF24 Rolling Code Cracker** (`crazyradio_nrf24_rolling_code_cracker.py`)
Captures rolling-code-based RF signals (garage doors, car key fobs).  
Attempts brute-force attacks on rolling codes for replay vulnerabilities.  
Predicts future rolling codes to bypass security.  

### **6️⃣ Adaptive Frequency-Hopping Sniffer** (`crazyradio_nrf24_fh_sniffer.py`)
Tracks and analyzes frequency-hopping NRF24 communications.  
Logs hopping sequences to map out channel-switching behavior.  
Integrates with MitM attack script for dynamic packet injection.  

### **7️⃣ NRF24 Man-in-the-Middle (MitM) Attacks** (`crazyradio_nrf24_mitm.py`)
Intercepts NRF24 traffic in real-time.  
Modifies or replays packets to manipulate devices.  
Bypasses authentication mechanisms using spoofed responses.  

### **8️⃣ Persistent Mouse/Keyboard Hijacker** (`crazyradio_persistent_hijacker.py`)
Maintains control over a hijacked Logitech keyboard/mouse indefinitely.  
Resends connection requests if the user tries to disconnect.  
Stores hijacked devices in a persistent session for later control.  

## Usage Examples
Run any script using Python:
```sh
python crazyradio_mousejack.py --scan
```

To sniff NRF24 packets:
```sh
python crazyradio_nrf24_sniffer.py --sniff --channel 76
```

To jam detected NRF24 devices:
```sh
python crazyradio_nrf24_jammer.py --jam --target XX:XX:XX:XX:XX:XX
```

## Disclaimer
🚨 **For educational & security testing purposes only!** 🚨  
Do **not** use these tools on unauthorized networks or devices.  
The author is **not responsible** for misuse or legal consequences.  

---
🔥 **Crazyradio 2.0 Hacking Toolkit** - Take RF security testing to the next level! 🚀


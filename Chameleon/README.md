# Chameleon Ultra Overview

The **Chameleon Ultra** is an **advanced RFID/NFC security research tool** designed for **cloning, emulation, and cracking** of high-frequency (HF) and low-frequency (LF) RFID systems. Developed for **penetration testers, red teams, and security researchers**, it provides powerful capabilities for analyzing and bypassing **access control systems, payment cards, and RFID-enabled devices**.

## **Key Features**

- **Frequency Support:**
  - **Low-Frequency (LF):** 125 kHz & 134 kHz (HID Prox, T5577, Indala, EM4100, etc.)
  - **High-Frequency (HF):** 13.56 MHz (MIFARE, DESFire, iClass, NFC, etc.)
- **Multi-Card Emulation:** Emulates multiple RFID card types **simultaneously**
- **Fast Read/Write:** Captures and clones RFID/NFC tags in **real-time**
- **Brute-Force & Key Cracking:** Supports **MIFARE Classic** and **iClass** key extraction
- **Standalone & PC Mode:** Works independently or with **RFID analysis software**
- **Battery-Powered:** Portable, with **USB-C charging and Bluetooth support**
- **RFID Skimming Protection:** Detects and defends against rogue RFID readers
- **Software Compatibility:** Works with **Chameleon UI, Proxmark3, NFC tools, and RFID research frameworks**

## **Use Cases in RFID/NFC Security**

The **Chameleon Ultra** is widely used for **testing and analyzing RFID/NFC security**. Below are some key applications:

### **1️⃣ RFID/NFC Sniffing & Data Logging**
- Captures **RFID/NFC authentication sequences** in real-time
- Stores **multiple RFID tag interactions** for analysis
- Works with **RFID forensic tools** for deep packet inspection

### **2️⃣ RFID Cloning & Emulation**
- Reads and **clones access control badges, key fobs, and NFC cards**
- Emulates **MIFARE, HID, Indala, and other card types** for bypassing security checkpoints
- Supports **multi-card emulation for advanced red team operations**

### **3️⃣ Brute-Force & Key Cracking**
- Extracts **MIFARE Classic encryption keys** using nested authentication attacks
- Supports **iClass & DESFire key extraction and replay attacks**
- Automates brute-force testing against **RFID access control systems**

### **4️⃣ Relay & Replay Attacks**
- Records and replays **RFID/NFC authentication sequences** for unauthorized access
- Exploits **weak RFID implementations in smart locks, payment systems, and keycards**
- Works as a **relay node in distance-bounding attacks**

### **5️⃣ RFID Skimming & Defense**
- Detects unauthorized RFID readers attempting to skim cards
- Tests **contactless payment security vulnerabilities**
- Works with **Faraday cages and signal-blocking techniques** for RFID defense

### **6️⃣ Smart Card & Payment System Analysis**
- Analyzes **EMV, NFC-based credit/debit cards, and transport cards**
- Explores vulnerabilities in **contactless payment processing**
- Works with **Proxmark3 and Wireshark for forensic analysis**

## **Software & Tools**
- **Chameleon UI:** Official tool for managing emulated RFID profiles
- **Proxmark3 Client:** Supports deeper RFID/NFC security testing
- **Wireshark for NFC:** Captures and analyzes NFC transactions
- **Bettercap RFID/NFC Modules:** Red teaming integration for automated attacks

# Chameleon Ultra - Advanced NFC Exploitation Toolkit

## Overview
The **Chameleon Ultra Toolkit** is a powerful NFC exploitation framework designed for red team operations, penetration testing, and security research. It provides advanced capabilities such as NFC tag spoofing, key cracking, replay attacks, relay exploits, and real-time monitoring.

## Features
- **Tag Emulation & Spoofing** – Clone and modify NFC tags dynamically.
- **Offline Key Cracking** – Perform brute-force attacks on captured NFC keys.
- **Replay Attack Automation** – Capture and replay NFC transactions at scale.
- **Advanced Encryption Bypass** – Decrypt and analyze encrypted NFC traffic.
- **Multi-Protocol Relay** – Relay NFC data to BLE, Wi-Fi, or Sub-1GHz.
- **Automated Attack Chaining** – Execute sequential exploits automatically.
- **Real-Time AI-Based Exploit Recommendations** – AI suggests optimal attack vectors.
- **SDR Integration for Passive NFC Monitoring** – Captures NFC signals for real-time intelligence.
- **NFC Anomaly Detection** – Detects malicious activity in NFC environments.
- **Bluetooth-NFC Relay Attacks** – Bridges Bluetooth & NFC for advanced exploits.
- **Cross-Protocol Exploit Chaining** – Executes attacks across NFC, Bluetooth, Wi-Fi, and RF.
- **Automated NFC Honeypot Deployment** – Captures and logs unauthorized NFC interactions.
- **UWB-Assisted Tracking** – Locates NFC-enabled devices using precise positioning.

## Installation
### Prerequisites
- **Python 3.x**
- **Chameleon Ultra device**
- **LibNFC / Proxmark3 / Chameleon Ultra CLI tools**
- **PyCryptodome** (for AES/DES decryption)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourrepo/chameleon-ultra-tools.git
   cd chameleon-ultra-tools
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Connect your **Chameleon Ultra** device.
4. Run commands as needed.

## Usage Examples

### 1. **Spoof an NFC tag dynamically**
```sh
python chameleon_tools.py --spoof --tag-type MIFARE --uid 123456
```

### 2. **Crack NFC keys offline**
```sh
python chameleon_tools.py --crack --input keys_dump.bin
```

### 3. **Replay a captured NFC transaction**
```sh
python chameleon_tools.py --replay --input captured_nfc.log
```

### 4. **Relay NFC data to another protocol (e.g., BLE, Wi-Fi)**
```sh
python chameleon_tools.py --relay --target BLE --input nfc_data.bin
```

### 5. **Deploy an NFC honeypot for logging unauthorized activity**
```sh
python chameleon_tools.py --honeypot --logfile nfc_attacks.log
```

### 6. **Execute automated attack chaining**
```sh
python chameleon_tools.py --auto-chain --input attack_sequence.json
```

### 7. **Monitor NFC traffic passively with SDR**
```sh
python chameleon_tools.py --sdr-monitor
```

### 8. **Detect NFC anomalies in real-time**
```sh
python chameleon_tools.py --detect-anomalies
```

### 9. **Fingerprint vulnerabilities in an NFC session**
```sh
python chameleon_tools.py --fingerprint --input captured_nfc.log
```

### 10. **Execute a Bluetooth-NFC relay attack**
```sh
python chameleon_tools.py --bt-nfc-relay --target XX:XX:XX:XX:XX:XX
```

### 11. **Execute cross-protocol exploit chaining**
```sh
python chameleon_tools.py --cross-chain --input attack_list.json
```

### 12. **Track NFC-enabled devices using UWB positioning**
```sh
python chameleon_tools.py --uwb-track --target XX:XX:XX:XX:XX:XX
```

## Disclaimer
This toolkit is intended for **authorized security testing and research purposes only**. Unauthorized use of these tools may violate laws and regulations. The authors are not responsible for any misuse or damages caused.

---
🚀 **Developed for professional penetration testers and cybersecurity researchers.**



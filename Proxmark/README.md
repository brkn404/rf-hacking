# Proxmark3 Overview

The **Proxmark3** is a **powerful RFID and NFC security research tool** used for analyzing, cloning, and cracking **high-frequency (HF) and low-frequency (LF) RFID/NFC systems**. It supports multiple RFID protocols and is widely used by **penetration testers, red teams, and security researchers** to test access control systems, payment cards, and RFID-enabled devices.

## **Key Features**

- **Frequency Support:**
  - **Low-Frequency (LF):** 125 kHz & 134 kHz (HID Prox, T5577, Indala, etc.)
  - **High-Frequency (HF):** 13.56 MHz (MIFARE, iClass, NFC, DESFire, etc.)
- **Modulation & Protocols:** Supports ASK, FSK, PSK, and various proprietary encodings
- **Card Emulation:** Emulates RFID/NFC tags for **bypassing access control**
- **Cloning & Replay Attacks:** Reads, saves, and replays RFID signals for **authentication bypass**
- **Brute-Force & Cracking:** Extracts encryption keys from **MIFARE Classic & iClass cards**
- **Proxmark3 Models:** Available in **Proxmark3 Easy, RDV4, and RDV4.01** with wireless capabilities
- **Software Compatibility:** Works with **Proxmark3 client, RFID tools, and NFC analyzers**

## **Use Cases in RFID/NFC Security**

The **Proxmark3** is commonly used for **analyzing and attacking RFID and NFC systems**. Below are some key applications:

### **1️⃣ RFID/NFC Sniffing & Reverse Engineering**
- Captures RFID/NFC **authentication sequences**
- Decodes proprietary protocols and reverse-engineers **unknown tag formats**

### **2️⃣ RFID Cloning & Emulation**
- Reads and **clones access badges, smart cards, and NFC tags**
- Emulates **MIFARE, HID, Indala, and other RFID cards**
- Bypasses security checkpoints and **physical access control systems**

### **3️⃣ Brute-Force & Key Cracking**
- Extracts **MIFARE Classic encryption keys**
- Uses **nested authentication attacks** to crack RFID cards
- Supports **iClass and DESFire key extraction**

### **4️⃣ Replay Attacks**
- Records and replays **RFID/NFC signals** for authentication bypass
- Exploits **poorly secured access control systems**

### **5️⃣ RFID/NFC Jamming & Detection**
- Detects RFID skimmers and rogue readers
- Jams weakly secured NFC devices

### **6️⃣ Payment Card & Smart Card Analysis**
- Analyzes **contactless payment systems** for security flaws
- Tests **EMV and NFC-based credit/debit card security**

## **Software & Tools**
- **Proxmark3 Client:** Official tool for reading, writing, and cracking RFID tags
- **RFID Research Tools:** Works with **MFOC, MFKey32, and LibNFC** for key extraction
- **Wireshark for NFC:** Used for analyzing captured NFC traffic
- **Bettercap & RFExploit:** Integrates with red teaming tools for automation


# Proxmark Hacking Toolkit

## Overview
The **Proxmark Hacking Toolkit** is a collection of scripts designed to extend the capabilities of the **Proxmark3** and other RFID/NFC penetration testing tools. These scripts enable **card cloning, relay attacks, brute-forcing, replay attacks, skimming, jamming, and vulnerability assessments** for **RFID, NFC, and credit card security testing**.

## Requirements
- **Proxmark3 RDV4** or **Proxmark3 Easy**
- **RFID/NFC-compatible cards or devices**
- **Python 3.x** (for automation scripts)
- **Required Libraries:** `pyscard`, `nfcpy`, `pycryptodome`

## Scripts & Features

### **1️⃣ RFID & NFC Card Cloning** (`rfid_card_cloning.py`)
- Reads and clones RFID/NFC cards (125kHz, 13.56MHz)
- Supports MIFARE Classic, MIFARE DESFire, and HID Prox
- Dumps card data for further analysis

### **2️⃣ RFID/NFC Brute-Forcing** (`rfid_mifare_bruteforce.py`)
- Attempts brute-force authentication on MIFARE Classic/DESFire
- Supports custom key dictionaries
- Logs successful key attempts for later use

### **3️⃣ NFC Relay Attacks** (`nfc_relay_attack.py`)
- Performs real-time relay attacks on NFC-based access control
- Works with **contactless payment systems, hotel keycards, and transit cards**

### **4️⃣ Advanced Credit Card Attacks** (`advanced_credit_card_attack.py`)
- Extracts card data from **EMV chip transactions**
- Captures transaction details for forensic analysis

### **5️⃣ Cracking Credit Card Data** (`cracking_credit_card_data.py`)
- Parses and analyzes **Track 1 & Track 2 data** from magstripe dumps
- Attempts CVV and PIN brute-forcing

### **6️⃣ EMV Transaction Tampering** (`emv_transaction_tampering.py`)
- Modifies intercepted EMV transaction data
- Attempts **unauthorized transaction replay**

### **7️⃣ RFID Sniffing & Analysis** (`rfid_sniffing.py`)
- Sniffs and captures RFID/NFC signals
- Analyzes captured data for security weaknesses

### **8️⃣ RFID/NFC Replay Attack Detection** (`rfid_replay_attack_detection.py`)
- Detects unauthorized replay attacks on RFID/NFC systems
- Monitors frequency patterns for **malicious attempts**

### **9️⃣ Smart Lock Vulnerability Testing** (`smart_lock_vulnerability_toolkit.py`)
- Scans and exploits weaknesses in **smart locks and access control**
- Works with **Bluetooth, NFC, and Zigbee-based locks**

### **🔟 RFID Tag Emulation** (`rfid_tag_emulation.py`)
- Emulates cloned RFID/NFC tags for **bypassing access control**
- Supports **Proxmark3, Chameleon Ultra, and Flipper Zero**

## Usage Examples

### Clone an RFID/NFC Card:
```sh
python rfid_card_cloning.py --read --save card_dump.bin
python rfid_card_cloning.py --write --load card_dump.bin
```

### Run a Relay Attack:
```sh
python nfc_relay_attack.py --target transit_card
```

### Detect Replay Attacks:
```sh
python rfid_replay_attack_detection.py --monitor
```

### Crack MIFARE Classic Keys:
```sh
python rfid_mifare_bruteforce.py --bruteforce
```

## Disclaimer
🚨 **For educational and security testing purposes only!** 🚨  
Do **not** use these tools on unauthorized systems. The author is **not responsible** for any misuse or legal consequences.

---
🔥 **Proxmark Hacking Toolkit** - Elevate RFID/NFC security testing! 🚀

Features of the Chameleon Ultra
1. Multi-Frequency Support:

    Supports LF (125 kHz) and HF (13.56 MHz) frequencies.

    Compatible with a wide range of RFID/NFC protocols, including:

        125 kHz: EM410x, HID Prox, Indala, and more.

        13.56 MHz: MIFARE Classic, MIFARE Ultralight, NTAG, DESFire, and more.

2. Emulation and Cloning:

    Emulate RFID/NFC tags in real-time.

    Clone existing tags and store them in the device’s memory.

3. Onboard Memory:

    Stores multiple tag profiles for quick switching between emulated tags.

4. Custom Firmware:

    Open-source firmware allows for customization and advanced use cases.

    Community-driven updates and enhancements.

5. Portable and Battery-Powered:

    Compact and portable design with a rechargeable battery.

    Ideal for field use and penetration testing.

6. User-Friendly Interface:

    OLED display for easy navigation and status updates.

    Button-based interface for quick operation.

7. USB Connectivity:

    Connects to a computer for firmware updates and advanced configuration.

Functions of the Chameleon Ultra
1. Tag Emulation:

    Emulate RFID/NFC tags to bypass access control systems.

    Useful for testing the security of RFID-based systems.

2. Tag Cloning:

    Clone existing RFID/NFC tags and store them for later use.

    Supports both read-only and read-write tags.

3. Tag Reading:

    Read and decode RFID/NFC tags to extract their data.

    Analyze tag data for vulnerabilities or cloning.

4. Tag Writing:

    Write data to writable RFID/NFC tags.

    Create custom tags for testing or access control.

5. Replay Attacks:

    Capture and replay RFID/NFC signals to bypass rolling code systems.

6. Brute-Force Attacks:

    Perform brute-force attacks on MIFARE Classic tags to recover keys.

Use Cases for the Chameleon Ultra
1. Penetration Testing:

    Test the security of RFID/NFC-based access control systems.

    Identify vulnerabilities in tag protocols and reader implementations.

2. Access Control Bypass:

    Clone or emulate legitimate RFID/NFC tags to gain unauthorized access.

    Test the effectiveness of access control systems.

3. Research and Development:

    Study RFID/NFC protocols and their security weaknesses.

    Develop custom tools and scripts for RFID/NFC manipulation.

4. Physical Security Audits:

    Audit the security of physical access systems (e.g., door locks, gates).

    Identify and mitigate risks associated with RFID/NFC systems.

5. Education and Training:

    Teach students and professionals about RFID/NFC security.

    Demonstrate real-world attacks and defenses.


    The Chameleon Ultra is a versatile and powerful tool for RFID/NFC emulation, cloning, and security testing. Its multi-frequency support, custom firmware, and portable design make it ideal for a wide range of use cases, from penetration testing to education. By building custom tools and scripts, you can extend its functionality and integrate it with other tools for advanced workflows.



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



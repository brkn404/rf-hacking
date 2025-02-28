Yard Stick One Overview

The Yard Stick One (YS1) is a sub-1GHz transceiver designed for security researchers and RF hackers. It’s based on the Texas Instruments CC1111 chip and is used for transmitting, receiving, and analyzing signals in the 300-928 MHz range.
Key Features

    Frequency Range: 300-928 MHz (configurable)
    Modulation: ASK, OOK, GFSK, MSK, 2-FSK, 4-FSK
    Transmission Power: Adjustable from low to high output
    Software Support: Compatible with rfcat, GNU Radio, and SDR frameworks
    Connectivity: USB interface with Python control via RfCat
    Supported Protocols: Commonly used in remote control systems, garage door openers, key fobs, industrial control systems, and IoT devices
    Operating Modes: Sniffing, transmitting, replaying, and brute forcing

Use Cases in RF Security

The Yard Stick One is commonly used for analyzing and attacking wireless protocols in the sub-1GHz range. Below are some key applications:

    Sniffing and Reverse Engineering:
        Capture wireless signals from key fobs, remotes, IoT devices, and alarm systems.
        Decode unknown protocols and identify vulnerabilities.

    Replay Attacks:
        Record transmissions from wireless devices and replay them to trigger actions (e.g., opening a garage door, unlocking a car).
        Common against unprotected RF key fobs and simple remote-controlled systems.

    Brute-Force Attacks:
        If a system uses a fixed set of codes, brute-force the key space to gain unauthorized access.
        Example: Attack outdated security systems with a predictable RF sequence.

    Jamming & Denial of Service:
        Disrupt communication between legitimate RF devices by transmitting noise.
        Used to disable alarms, prevent remote controls from functioning, or block IoT sensors.

    Man-in-the-Middle (MitM) & Injection:
        Modify and resend signals to impersonate a device.
        Example: Inject custom packets into wireless devices for unauthorized control.

    Smart Meter & Industrial Control System (ICS) Exploits:
        Many industrial and smart meter systems use sub-GHz frequencies for data transmission.
        These signals can be sniffed, modified, and replayed for potential exploits.




# Yard Stick One RF Toolkit

This repository contains various scripts designed for **RF security analysis, pentesting, and research** using the **Yard Stick One (YS1)** hardware. The scripts allow for **sniffing, injecting, jamming, and analyzing** wireless signals across different frequency bands.

## **Table of Contents**
- [Requirements](#requirements)
- [Installation](#installation)
- [Scripts Overview](#scripts-overview)
- [Usage](#usage)
- [Disclaimer](#disclaimer)

---

## **Requirements**
### **Hardware:**
- [Yard Stick One (Great Scott Gadgets)](https://greatscottgadgets.com/yardstickone/)

### **Software & Dependencies:**
- Python 3.x
- `rfcat` (for interfacing with YS1)
- `numpy`, `matplotlib` (for signal analysis & visualization)
- `json` (for logging and data storage)

To install dependencies:
```sh
pip install numpy matplotlib
```

---

## **Scripts Overview**
Each script serves a specific purpose in RF security testing. Below is a breakdown of the functionality:

### **1️⃣ RF Sniffing & Signal Analysis**
- **`yardstick_sniffer.py`** – Captures and logs RF signals for analysis.
- **`yardstick_signal_analyzer.py`** – Analyzes RF signal waveforms, modulation schemes, and patterns.

### **2️⃣ RF Transmission & Injection**
- **`yardstick_packet_injector.py`** – Injects arbitrary RF packets for testing wireless security.
- **`yardstick_replay.py`** – Captures and replays RF transmissions (useful for testing security vulnerabilities).
- **`yardstick_mitm_relay.py`** – Man-in-the-Middle (MitM) tool that captures and modifies RF signals before retransmitting.

### **3️⃣ RF Jamming & Disruption**
- **`yardstick_jammer.py`** – Sends noise on a target frequency to disrupt RF communication.

### **4️⃣ Rolling Codes & Brute-Forcing**
- **`yardstick_rolling_code_cracker.py`** – Captures and predicts rolling codes for garage doors, car remotes, and similar systems.
- **`yardstick_bruteforce.py`** – Attempts brute-force attacks against RF-based security mechanisms.

### **5️⃣ Industrial & IoT Security Testing**
- **`yardstick_smart_meter.py`** – Captures and analyzes **smart meter** transmissions, looking for injection vulnerabilities.
- **`yardstick_ics_testing.py`** – Tests **industrial control systems (ICS) and SCADA** devices for RF security flaws.

### **6️⃣ RFID & NFC Spoofing**
- **`yardstick_beacon_spammer.py`** – Captures and spoofs **RFID/NFC beacons** for proximity attacks.

### **7️⃣ RF Scanning & Wideband Analysis**
- **`yardstick_frequency_scanner.py`** – Scans a range of frequencies for active RF transmissions.
- **`yardstick_long_range_scanner.py`** – **Broadband** scanner that logs **signal activity, RSSI, and peak usage times**.

---

## **Usage**
Each script includes detailed **usage instructions**. Run any script with `--help` to view available options.

Example: Capturing RF signals at **433.92 MHz**:
```sh
python yardstick_sniffer.py --freq 433920000
```

Example: Scanning a frequency range from **300 MHz to 928 MHz**:
```sh
python yardstick_long_range_scanner.py --start 300000000 --stop 928000000 --step 1000000 --log scan_results.json
```

---

## **Disclaimer**
🚨 **This repository is for educational and research purposes only.** 🚨
Using these tools on networks or devices **without explicit authorization** is **illegal**. Ensure compliance with all local laws and regulations before testing any RF systems.

**Use responsibly. You are responsible for your actions.** 🔥

---

Let me know if you need additional refinements! 🚀


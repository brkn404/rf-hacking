# Yard Stick One Overview

The **Yard Stick One (YS1)** is a sub-1GHz transceiver designed for security researchers and RF hackers. It’s based on the **Texas Instruments CC1111** chip and is used for transmitting, receiving, and analyzing signals in the **300-928 MHz** range.

## **Key Features**

- **Frequency Range:** 300-928 MHz (configurable)
- **Modulation:** ASK, OOK, GFSK, MSK, 2-FSK, 4-FSK
- **Transmission Power:** Adjustable from low to high output
- **Software Support:** Compatible with `rfcat`, `GNU Radio`, and `SDR` frameworks
- **Connectivity:** USB interface with Python control via `RfCat`
- **Supported Protocols:** Used in **remote control systems, garage door openers, key fobs, industrial control systems, and IoT devices**
- **Operating Modes:** **Sniffing, transmitting, replaying, and brute-forcing**

## **Use Cases in RF Security**

The **Yard Stick One** is commonly used for analyzing and attacking **wireless protocols in the sub-1GHz range**. Below are some key applications:

### **1️⃣ Sniffing and Reverse Engineering**
- Capture wireless signals from **key fobs, remotes, IoT devices, and alarm systems**
- Decode unknown protocols and identify vulnerabilities

### **2️⃣ Replay Attacks**
- Record transmissions from wireless devices and replay them to trigger actions (**e.g., opening a garage door, unlocking a car**)
- Common against unprotected **RF key fobs and simple remote-controlled systems**

### **3️⃣ Brute-Force Attacks**
- If a system uses a fixed set of codes, **brute-force the key space** to gain unauthorized access
- Example: Attack outdated **security systems with predictable RF sequences**

### **4️⃣ Jamming & Denial of Service**
- Disrupt communication between **legitimate RF devices** by transmitting noise
- Used to **disable alarms, prevent remote controls from functioning, or block IoT sensors**

### **5️⃣ Man-in-the-Middle (MitM) & Injection**
- Modify and resend signals to **impersonate a device**
- Example: Inject custom packets into wireless devices for **unauthorized control**

### **6️⃣ Smart Meter & Industrial Control System (ICS) Exploits**
- Many industrial and **smart meter systems use sub-GHz frequencies for data transmission**
- These signals can be **sniffed, modified, and replayed** for potential exploits

---

# **Yard Stick One RF Toolkit**

## **Overview**
The **Yard Stick One RF Toolkit** is a collection of scripts designed to **extend the capabilities** of the **Yard Stick One (YS1)** for **sub-1GHz RF security analysis, penetration testing, and signal manipulation**. These tools allow for **sniffing, jamming, replay attacks, brute-forcing, and signal injection** beyond traditional RF tools.

## **Requirements**
- **Yard Stick One (YS1)** (Great Scott Gadgets)
- **Python 3.x**
- **Required Libraries:** `rfcat`, `numpy`, `matplotlib`

## **Scripts & Features**

### **1️⃣ RF Sniffing & Signal Analysis**
- **`yardstick_sniffer.py`** – Captures and logs RF signals for analysis.
- **`yardstick_signal_analyzer.py`** – Analyzes RF signal waveforms, modulation schemes, and patterns.

### **2️⃣ RF Transmission & Injection**
- **`yardstick_packet_injector.py`** – Injects arbitrary RF packets for testing wireless security.
- **`yardstick_replay.py`** – Captures and replays RF transmissions (useful for security testing).
- **`yardstick_mitm_relay.py`** – Man-in-the-Middle (MitM) tool that captures and modifies RF signals before retransmitting.

### **3️⃣ RF Jamming & Disruption**
- **`yardstick_jammer.py`** – Sends noise on a target frequency to disrupt RF communication.

### **4️⃣ Rolling Codes & Brute-Forcing**
- **`yardstick_rolling_code_cracker.py`** – Captures and predicts rolling codes for garage doors, car remotes, and similar systems.
- **`yardstick_bruteforce.py`** – Attempts brute-force attacks against RF-based security mechanisms.

### **5️⃣ Industrial & IoT Security Testing**
- **`yardstick_smart_meter.py`** – Captures and analyzes **smart meter** transmissions, looking for injection vulnerabilities.
- **`yardstick_ics_testing.py`** – Tests **industrial control systems (ICS) and SCADA** devices for RF security flaws.

### **6️⃣ RF Scanning & Wideband Analysis**
- **`yardstick_frequency_scanner.py`** – Scans a range of frequencies for active RF transmissions.
- **`yardstick_long_range_scanner.py`** – **Broadband** scanner that logs **signal activity, RSSI, and peak usage times**.

### **7️⃣ Bluetooth & Keystroke Attacks**
- **`blueducky.py`** – Uses RF to attack Bluetooth and USB HID devices.
- **`yardstick_blueducky_keystroke_hijacker.py`** – Captures and injects keystrokes from vulnerable HID devices.
- **`yardstick_keystroke_hijacker.py`** – Injects malicious keystrokes into wireless keyboards.

## **Usage Examples**

### Capture RF signals at **433.92 MHz**:
```sh
python yardstick_sniffer.py --freq 433920000
```

### Scan a frequency range from **300 MHz to 928 MHz**:
```sh
python yardstick_long_range_scanner.py --start 300000000 --stop 928000000 --step 1000000 --log scan_results.json
```

### Inject a captured RF packet:
```sh
python yardstick_packet_injector.py --file captured_signal.bin
```

### Run a Bluetooth Keystroke Hijack Attack:
```sh
python yardstick_keystroke_hijacker.py --target keyboard_device
```

## **Disclaimer**
🚨 **For educational and security testing purposes only!** 🚨  
Do **not** use these tools on unauthorized systems. The author is **not responsible** for any misuse or legal consequences.

---
🔥 **Yard Stick One RF Toolkit** - Expanding RF penetration testing! 🚀

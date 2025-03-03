# ESP8266 Overview

The **ESP8266** is a low-cost, **Wi-Fi-enabled microcontroller** developed by **Espressif Systems**. It is widely used for **IoT projects, wireless security testing, and network penetration testing** due to its compact size, powerful features, and ability to operate as a **Wi-Fi client, access point, or packet injection tool**.

## **Key Features**

- **Wi-Fi Support:** 802.11 b/g/n (2.4 GHz)
- **Processor:** 32-bit Tensilica L106, running at 80-160 MHz
- **Memory:** 64 KB RAM, 4 MB Flash (varies by model)
- **Operating Modes:** Client, SoftAP, Promiscuous mode
- **Network Security Testing:** Supports **deauthentication, sniffing, replay attacks, and rogue APs**
- **Power Efficiency:** Low-power operation with deep sleep support
- **Connectivity:** UART, SPI, I2C, PWM, ADC
- **Programming Support:** Works with **Arduino IDE, MicroPython, and AT commands**

## **Use Cases in Wireless Security**

The **ESP8266** is commonly used for **Wi-Fi penetration testing and IoT security analysis**. Below are some key applications:

### **1️⃣ Wi-Fi Sniffing & Packet Injection**
- Captures **unencrypted Wi-Fi packets** in monitor mode
- Injects malicious packets into Wi-Fi traffic for **exploitation testing**
- Works with **Wireshark and Bettercap** for traffic analysis

### **2️⃣ Wi-Fi Deauthentication & Jamming Attacks**
- Performs **Wi-Fi deauth attacks** to disconnect users from a network
- Used for **testing WPA/WPA2 security and rogue AP detection**
- Disrupts specific clients without affecting the entire network

### **3️⃣ Rogue Access Point (Evil Twin Attacks)**
- Creates a **fake Wi-Fi network** that mimics real SSIDs
- Captures **credentials and user traffic** for penetration testing
- Uses **ESP8266 Deauther and Bettercap** for automation

### **4️⃣ IoT Device Security Testing**
- Exploits insecure **IoT devices and smart home networks**
- Sniffs **MQTT, CoAP, and HTTP traffic** from IoT devices
- Tests **weak authentication mechanisms in smart home devices**

### **5️⃣ WPA Handshake Capture & Dictionary Attacks**
- Captures **WPA/WPA2 handshakes for offline cracking**
- Automates handshake logging for **brute-force testing**
- Integrates with **Hashcat and Aircrack-ng** for password recovery

### **6️⃣ Wi-Fi Network Scanning & Reconnaissance**
- Scans for **Wi-Fi networks, connected devices, and open ports**
- Logs SSIDs, MAC addresses, signal strength (RSSI), and security protocols
- Helps identify **vulnerable networks and misconfigured access points**

## **Software & Tools**
- **ESP8266 Deauther:** Wi-Fi penetration testing framework
- **Bettercap & Aircrack-ng:** Wireless attack automation
- **Wireshark & tcpdump:** Packet capture and network forensics
- **ESPHome & MicroPython:** IoT and automation scripting

# ESP8266 Wireless Attack & Tracking Toolkit

## 📌 Overview
This toolkit utilizes an ESP8266 module for **Wi-Fi attacks, signal tracking, and network reconnaissance**. It includes multiple scripts for deauthentication attacks, SSID flooding, MAC spoofing, rogue access points, and **proximity tracking** via RSSI measurements. These tools allow penetration testers and researchers to analyze and manipulate Wi-Fi networks effectively.

## 📡 Supported Scripts

### 1️⃣ **ESP8266 - Proximity Tracker** (`esp8266_proximity_tracker.py`)
**Tracks specific MAC addresses based on RSSI movement.**
- Monitor device proximity by analyzing signal strength variations.
- Enable **live tracking with real-time graphing**.
- **Log movement patterns** for later analysis.

📌 **Usage:**
```sh
python esp8266_proximity_tracker.py --track XX:XX:XX:XX:XX:XX --live
```

### 2️⃣ **ESP8266 - RSSI Heatmap & Signal Strength Mapper** (`esp8266_heatmap.py`)
**Scans and maps Wi-Fi signal strength for attack positioning.**
- Generates a **heatmap of RSSI values**.
- **Recommends attack strategies** based on signal strength.
- **Finds optimal attack paths** and access points.
- Supports **automated AP hopping & attack path visualization**.

📌 **Usage:**
```sh
python esp8266_heatmap.py --scan --duration 60
```

### 3️⃣ **ESP8266 - Whitelist Bypass & MAC Spoofing** (`esp8266_whitelist_bypass.py`)
**Bypasses MAC filtering to gain network access.**
- **Scans for authorized devices** and spoofs their MAC addresses.
- **Automatically cycles MAC addresses** to avoid detection.
- **Detects networks with MAC-based access control**.

📌 **Usage:**
```sh
python esp8266_whitelist_bypass.py --auto --cycle 30
```

### 4️⃣ **ESP8266 - Beacon Spammer & SSID Confusion Tool** (`esp8266_beacon_spammer.py`)
**Floods Wi-Fi environments with fake SSIDs for deception.**
- **Generates randomized SSIDs**.
- **Mimics real networks** to confuse users.
- **Multi-channel broadcasting** to increase attack surface.

📌 **Usage:**
```sh
python esp8266_beacon_spammer.py --random --count 50
```

### 5️⃣ **ESP8266 - Automated Attack Chaining** (`esp8266_auto_attack.py`)
**Runs multiple Wi-Fi attack techniques in sequence.**
- Chains deauth, SSID flooding, Evil Twin, and MITM attacks.
- **Randomizes execution for stealth**.
- **Logs attack results** for analysis.

📌 **Usage:**
```sh
python esp8266_auto_attack.py --full --log
```

### 6️⃣ **ESP8266 - Rogue AP & Evil Twin Attack** (`esp8266_rogue_ap.py`)
**Creates fake access points to capture credentials.**
- **Clones legitimate SSIDs** for deception.
- Supports **captive portals for phishing**.
- **Integrates with MITM attacks** to intercept traffic.

📌 **Usage:**
```sh
python esp8266_rogue_ap.py --ssid "FreeWiFi" --captive-portal
```

---

## ⚡ Requirements
- **ESP8266 / ESP-01S** module
- **Python 3.x**
- **Matplotlib** (for visualization)
- **PySerial** (for ESP8266 communication)

📌 **Install dependencies:**
```sh
pip install matplotlib pyserial
```

---

## ⚠️ Disclaimer
This toolkit is intended for **educational and research purposes only**. Unauthorized use of these scripts on networks you do not own or have explicit permission to test **is illegal**. Use responsibly! ⚠️

---

💡 **Next Steps:** Would you like additional **automated reporting** or **alerting features** in these tools? 🚀

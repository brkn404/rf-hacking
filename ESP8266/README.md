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

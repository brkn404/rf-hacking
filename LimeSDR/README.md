# LimeSDR & SDR Toolset

This repository contains various scripts for security research, signal analysis, and attack automation using **LimeSDR Mini 2.0** and other SDR devices.

## 📡 Features
✅ **Full-Spectrum RF Signal Scanning** (10 MHz - 3.5 GHz)  
✅ **GSM/LTE IMSI Catching & Rogue Base Station**  
✅ **Bluetooth/BLE Sniffing & Injection**  
✅ **Wi-Fi Exploitation (Deauth, MITM, Packet Injection)**  
✅ **GPS Spoofing & Navigation Attacks**  
✅ **ADS-B Aircraft Spoofing & Aviation Interference**  
✅ **RF Jamming & Denial-of-Service Attacks**  
✅ **Passive Keyless Entry (PKE) Exploitation for Vehicles**  
✅ **Covert RF Data Exfiltration (FM, LoRa, BLE, AM)**  
✅ **IoT & Industrial RF Attacks (Zigbee, LoRa, SCADA)**  

## 📂 Script Overview

### **LimeSDR-Specific Scripts**

| Script | Description |
|--------|-------------|
| **limesdr_lte_emulator.py** | Simulates & intercepts LTE signals, rogue cell tower attacks |
| **limesdr_pke_exploit.py** | Captures & replays signals from keyless car fobs, garage doors |
| **limesdr_radio_transmitter.py** | Transmits FM/AM/SSB radio messages & covert audio |
| **limesdr_rf_exfiltration.py** | Leaks data via RF using stego, LoRa, BLE, and more |
| **limesdr_satellite_sniffer.py** | Captures signals from GPS, Iridium, Inmarsat satellites |
| **limesdr_spectrum_analyzer.py** | Monitors spectrum & detects unauthorized transmissions |
| **limesdr_voice_decoder.py** | Decodes TETRA, P25, DMR digital radio communications |

### **General SDR Attack Scripts**

| Script | Description |
|--------|-------------|
| **sdr_adsb_spoof.py** | Spoofs aircraft locations on ATC radar |
| **sdr_auto_pwn.py** | Automates cross-protocol MITM attacks (GSM, Wi-Fi, Bluetooth) |
| **sdr_bt_hijack.py** | Hijacks & injects Bluetooth packets into active connections |
| **sdr_gps_spoof.py** | Transmits fake GPS signals to manipulate location services |
| **sdr_imsi_catcher.py** | Captures IMSI/IMEI numbers, intercepts GSM communications |
| **sdr_iot_exploit.py** | Exploits LoRa, Zigbee, SCADA, & industrial RF systems |
| **sdr_replay_attack.py** | Records & replays RF signals for remote controls, alarms |
| **sdr_rf_jammer.py** | Jams Bluetooth, Wi-Fi, GSM, & IoT frequencies |
| **sdr_rf_scanner.py** | Scans RF spectrum & detects active transmissions |
| **sdr_wifi_attack.py** | Wi-Fi exploitation: deauth, MITM, rogue AP, credential capture |

## ⚙️ Setup

1️⃣ **Install Required Dependencies:**  
```bash
sudo apt update && sudo apt install -y gnuradio soapy-sdr limeutils aircrack-ng wireshark
```

2️⃣ **Install SDR Software:**  
```bash
pip install soapy_power stegoRF srsLTE gr-bluetooth
```

3️⃣ **Connect Your SDR & Verify:**  
```bash
SoapySDRUtil --find
```

## 🔥 Example Usage

🔹 **Scan RF Spectrum for Active Signals:**  
```bash
python sdr_rf_scanner.py --freq-start 50M --freq-end 3.5G
```

🔹 **Intercept & Modify Bluetooth Communications:**  
```bash
python sdr_bt_hijack.py --scan --inject "Hello World"
```

🔹 **Rogue LTE Base Station:**  
```bash
python limesdr_lte_emulator.py --start --freq 850M
```

🔹 **Jam Nearby Wi-Fi Networks:**  
```bash
python sdr_wifi_attack.py --deauth --target 00:11:22:33:44:55
```

🔹 **Covert RF Data Exfiltration (Stego & LoRa):**  
```bash
python limesdr_rf_exfiltration.py --stego --lora --file secret.txt
```

## 🚀 Disclaimer
**For educational and research purposes only.** Unauthorized use of these tools may violate laws and regulations. The user assumes all responsibility.

---

### **What’s Next?**
Would you like **automated frequency-hopping attacks**, **coordinated multi-device attacks**, or **custom SDR fuzzing tools?** 🚀


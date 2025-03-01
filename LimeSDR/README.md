# **LimeSDR Mini 2.0 - Toolset for Wireless Security and Exploitation**

The **LimeSDR Mini 2.0** is a powerful Software Defined Radio (SDR) that allows for the analysis and exploitation of various wireless communication protocols. This toolkit provides a wide range of scripts designed for **security analysis**, **penetration testing**, and **research** purposes. It supports a variety of wireless protocols, including **Wi-Fi**, **Bluetooth**, **GSM/LTE**, **IoT**, and more.

## **📡 Key Features:**
- Full-spectrum RF scanning (10 MHz - 3.5 GHz)
- IMSI catching and rogue base stations
- Bluetooth sniffing, injection, and MITM
- Wi-Fi deauthentication, MITM, and packet injection
- Covert RF data exfiltration (FM, LoRa, BLE)
- GSM/LTE attack automation
- GPS spoofing and navigation attacks
- Satellite signal sniffing

---

## **📂 Script Overview**

### **LimeSDR-Specific Scripts:**

1. **`limesdr_lte_emulator.py`**  
   - Simulates and creates a **rogue LTE base station**, enabling **man-in-the-middle** (MITM) attacks on mobile devices and testing LTE vulnerabilities.

2. **`limesdr_pke_exploit.py`**  
   - Captures and replays signals from **keyless entry** systems such as **vehicles** and **garage doors**, enabling **unauthorized access**.

3. **`limesdr_radio_transmitter.py`**  
   - Transmits **FM**, **AM**, and **SSB** signals for **covert communication** or testing communication systems, providing a versatile signal transmission tool.

4. **`limesdr_rf_exfiltration.py`**  
   - Facilitates **covert RF data exfiltration** using **steganography** over RF channels (LoRa, BLE, FM, AM) for secure data transfer.

5. **`limesdr_satellite_sniffer.py`**  
   - Sniffs and captures signals from **satellite communication networks**, including **GPS**, **Iridium**, and **Inmarsat** satellites, useful for satellite signal analysis.

6. **`limesdr_spectrum_analyzer.py`**  
   - Scans the **RF spectrum** and detects **unauthorized transmissions** to analyze signal activity across various frequencies.

7. **`limesdr_voice_decoder.py`**  
   - Decodes and intercepts **TETRA**, **P25**, and **DMR** digital radio communications, enabling **eavesdropping** on critical voice transmissions.

---

### **General SDR Attack Scripts:**

1. **`sdr_adsb_spoof.py`**  
   - Spoofs **ADS-B** signals, which are used for **aircraft tracking** and **control**, enabling interference with air traffic control systems.

2. **`sdr_auto_pwn.py`**  
   - Automates **cross-protocol MITM attacks** (GSM, Wi-Fi, Bluetooth, IoT), providing a seamless exploitation workflow across wireless systems.

3. **`sdr_bt_hijack.py`**  
   - Hijacks **Bluetooth packets** in an active connection, allowing for **packet manipulation** and **MITM attacks** on Bluetooth devices.

4. **`sdr_gps_spoof.py`**  
   - Transmits **fake GPS signals**, enabling location manipulation for **GPS spoofing** attacks on navigation and tracking systems.

5. **`sdr_imsi_catcher.py`**  
   - Captures **IMSI/IMEI** numbers from **mobile devices**, enabling **device tracking** or **eavesdropping** on GSM communications.

6. **`sdr_iot_exploit.py`**  
   - Exploits vulnerabilities in **IoT** devices, targeting **Zigbee**, **LoRa**, **SCADA**, and other industrial IoT systems for remote attacks.

7. **`sdr_rf_jammer.py`**  
   - Jams multiple wireless frequencies (**Wi-Fi**, **Bluetooth**, **GSM**, **IoT**) to disrupt communication and perform **Denial of Service** (DoS) attacks.

8. **`sdr_replay_attack.py`**  
   - Records and replays **RF signals** from devices such as **remote controls**, alarms, or IoT systems to gain **unauthorized access** or control.

9. **`sdr_rf_scanner.py`**  
   - Scans the **RF spectrum** to detect **active signals** and identify potential vulnerabilities or rogue transmissions.

10. **`sdr_wifi_attack.py`**  
   - Exploits **Wi-Fi networks**, performing attacks such as **deauthentication**, **MITM**, rogue access points, and **credential capture**.

---

## **📋 Example Usage**

#### **Scan RF Spectrum for Active Signals:**

python limesdr_spectrum_analyzer.py --start-freq 100M --end-freq 3.5G

Simulate Rogue LTE Base Station:

python limesdr_lte_emulator.py --freq 850M

Hijack Bluetooth Communications:

python sdr_bt_hijack.py --scan --inject "Malicious Payload"

Covert Data Exfiltration Using LoRa:

python limesdr_rf_exfiltration.py --stego --lora --file secret_data.txt

Wi-Fi Network Attack (Deauthentication):

python sdr_wifi_attack.py --deauth --target "00:11:22:33:44:55"

Interception of Satellite Signals:

python limesdr_satellite_sniffer.py --freq 1.5G --protocol GPS

Spoof ADS-B Signals for Aircraft:

python sdr_adsb_spoof.py --freq 1090M

Perform Automated Attack on IoT Devices:

python sdr_auto_pwn.py --target "IoT Device" --attack-type "MITM"

Intercept and Decode Voice Communication (TETRA):

python limesdr_voice_decoder.py --decode TETRA

🚨 Legal Disclaimer:

This toolset is intended for ethical hacking, security research, and educational purposes only. Unauthorized use of these tools may violate laws and regulations. The user assumes all responsibility for their actions.
🔧 Setup Instructions

Install Required Dependencies: Ensure your system is updated and install necessary packages:

sudo apt-get update && sudo apt-get install -y gnuradio soapy-sdr limeutils aircrack-ng wireshark

Install SDR Libraries: Install SDR-specific libraries:

pip install soapy_power stegoRF srsLTE gr-bluetooth



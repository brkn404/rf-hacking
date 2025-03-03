# **📡 BTS Attack Control Suite**

## **📌 Overview**
The **BTS Attack Control Suite** is an advanced **cellular attack framework** designed to **deploy, monitor, and control** cellular-based security research tools. This suite allows security professionals and researchers to test network vulnerabilities by simulating **rogue base stations (BTS), IMSI catching, RF replay attacks, SS7 exploits, and real-time spectrum analysis**.

With an **integrated web-based dashboard and API**, users can **start, stop, and monitor attacks remotely**, making it an all-in-one solution for **mobile network security testing**.

---

## **🔥 Features**
### **1️⃣ Rogue LTE/GSM Base Station**
✅ Deploys a **fake cellular base station** using **srsRAN/OpenBTS**.  
✅ Can **force nearby devices to connect** for **call & SMS interception**.  
✅ Logs BTS activity and connections **in real time**.  

### **2️⃣ IMSI Catcher & Location Tracking**
✅ Captures **IMSI/IMEI numbers** from nearby mobile devices.  
✅ Queries **HLR/VLR lookup APIs** for **real-time tracking**.  
✅ Logs captured IMSIs for **historical tracking**.  

### **3️⃣ RF Spectrum Analyzer**
✅ Scans and **detects active signals** (LTE, GSM, Wi-Fi, etc.).  
✅ Identifies **rogue BTS towers & jamming attacks**.  
✅ Logs detected frequencies for **threat monitoring**.  

### **4️⃣ RF Replay Attack Module**
✅ Records and **replays RF authentication signals**.  
✅ Useful for **testing signal replay vulnerabilities** in IoT devices & GSM authentication.  
✅ Fully automated **record/replay loop**.  

### **5️⃣ SS7 Silent SMS & Call Redirection**
✅ Sends **stealth SMS messages** to track device location.  
✅ Redirects **incoming & outgoing calls** via **SS7 exploits**.  
✅ Supports **silent tracking without alerting the target**.  

### **6️⃣ Web-Based UI & API**
✅ Full **web-based control panel** for launching & monitoring attacks.  
✅ **REST API** to trigger attacks from **external systems**.  
✅ Stores **detailed attack logs** in an **SQLite database**.  

---

## **🛠️ Equipment & Software Requirements**

### **🔹 Hardware**
- **LimeSDR Mini / HackRF One / USRP B210** (For BTS, IMSI Catching, RF Analysis)  
- **Raspberry Pi 5 / x86 Linux Machine** (For running the software)  
- **Alfa Wi-Fi Adapter** (Optional, for network monitoring)  

### **🔹 Software**
- **Flask** (for Web API & UI): `pip install flask`  
- **srsRAN (formerly srsLTE)** (for LTE/GSM BTS)  
- **gr-gsm** (for IMSI Catching)  
- **HackRF tools** (for RF Replay)  
- **Wireshark + GSMTAP** (for monitoring & packet analysis)  
- **UHD** (for RF Spectrum Analysis)  
- **SQLite3** (for Logging & Data Storage)  
- **SS7 API** (for Silent SMS & Call Redirection, if available)  

---

## **🚀 Installation & Usage**
### **1️⃣ Install Dependencies**
```bash
pip install flask
sudo apt install sqlite3 gr-gsm srsran hackrf uhd wireshark
```

### **2️⃣ Run the BTS Attack Suite**
```bash
python3 bts_attack_control_suite.py
```

### **3️⃣ Access the Web UI**
- Open **`http://<your-ip>:5000`** in your browser.
- Monitor attacks, view logs, and control **rogue BTS, IMSI catcher, RF analysis, and SS7 exploits**.

---

## **📡 API Usage Examples**
### **Start a Rogue BTS**
```bash
curl -X POST http://<your-ip>:5000/start_bts -H "Content-Type: application/json" -d '{"band": "900"}'
```
### **Start IMSI Catcher**
```bash
curl -X POST http://<your-ip>:5000/start_imsi
```
### **Redirect a Call via SS7**
```bash
curl -X POST http://<your-ip>:5000/redirect_call -H "Content-Type: application/json" -d '{"imsi": "310150123456789", "redirect_to": "+15555555555"}'
```

---

## **📜 Logging & UI**
### **View Attack Logs via API**
```bash
curl -X GET http://<your-ip>:5000/logs
```
📌 Returns **last 10 attack logs**.

📡 **For advanced security research, penetration testing, and network vulnerability assessments!** 🚀


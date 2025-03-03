# **SS7 Exploit Suite - README**

## **📌 Overview: What is SS7?**
**Signaling System No. 7 (SS7)** is a global telecommunications protocol suite that enables networks to communicate for call setup, SMS, and location tracking. Originally designed in the 1970s, **SS7 lacks built-in security** and is vulnerable to numerous attacks, including:

- **IMSI Tracking** – Identifying and tracking mobile users.
- **Call and SMS Interception** – Redirecting voice calls and SMS messages.
- **Silent SMS Location Tracking** – Using stealth messages to get a device's real-time location.
- **LTE Downgrade Attacks** – Forcing devices to fall back to weaker 2G networks.
- **SIM-based Exploits** – Intercepting and replaying SIM authentication data.

## **🚀 Exploiting SS7: Attack Vectors**
This suite automates SS7 attacks through a **Flask-based web dashboard**, integrating **IMSI catching, rogue BTS deployment, LTE jamming, silent SMS tracking, and SIM authentication replay**.

### **1️⃣ IMSI Catching & Tracking**
- Captures **IMSI (International Mobile Subscriber Identity)** numbers from nearby devices.
- Identifies the **carrier, country, and device presence**.
- Stores captured IMSI data for tracking analysis.

### **2️⃣ Rogue BTS (Fake Cell Tower) for Call/SMS Interception**
- Deploys a **fake GSM base station** (2G/3G) using OpenBTS/YateBTS.
- Tricks mobile phones into connecting and intercepts **calls & SMS**.
- Can modify and reroute SMS messages.

### **3️⃣ LTE Downgrade & Jamming**
- **Jams LTE frequencies**, forcing phones to **fall back to 2G/3G**.
- Exploits **weak 2G encryption** to intercept traffic.
- Works with SDRs (Software Defined Radios) like **LimeSDR, HackRF, and AntSDR**.

### **4️⃣ Silent SMS Attack (Location Tracking)**
- Sends **stealthy SMS pings** that do not alert the target.
- Uses SS7 vulnerabilities to **retrieve a phone’s real-time location**.
- Results are stored and displayed in the web UI.

### **5️⃣ SIM-based SS7 Authentication Replay**
- Captures and replays **SIM authentication requests**.
- Can be used to **impersonate a SIM** on the network.
- Requires **Proxmark3 or Sysmocom SIMtrace2** for SIM sniffing.

---

## **🛠️ Required Hardware & Software**
### **✅ Hardware Needed:**
- **LimeSDR Mini / HackRF One / AntSDR E200** – For SDR-based attacks.
- **Proxmark3 / Sysmocom SIMtrace2** – For SIM-based SS7 attacks.
- **Raspberry Pi 5 / Mac Mini** – Ideal for running the exploit suite.
- **Alfa Wi-Fi Adapter** – Optional, for additional network attacks.

### **✅ Software Used:**
- **Flask (Python)** – For the Web Dashboard.
- **gr-gsm / Kalibrate** – For GSM IMSI catching.
- **YateBTS / OpenBTS** – For rogue cell tower deployment.
- **srsRAN (formerly srsLTE)** – For LTE downgrade & attack simulation.
- **Wireshark** – Integrated for real-time traffic monitoring.

---

## **🔧 Installation & Setup**
### **1️⃣ Install Required Dependencies**
```bash
sudo apt update && sudo apt install -y python3 python3-pip git
pip3 install flask requests
```

### **2️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/ss7-exploit-suite.git
cd ss7-exploit-suite
```

### **3️⃣ Start the Web Dashboard**
```bash
python3 ss7_exploit_dashboard.py
```
- **Access UI at:** `http://<your-ip>:5000`
- **Trigger Attacks from the Web Interface**.

### **4️⃣ Run an Attack via API**
Example: Start IMSI Catcher remotely:
```bash
curl -X POST http://<your-ip>:5000/run_attack -H "Content-Type: application/json" -d '{"attack": "imsi_catcher"}'
```

### **5️⃣ View Logs & Captured Data**
```bash
curl -X GET http://<your-ip>:5000/get_logs
```
- Displays **IMSI Captures, Silent SMS logs, and LTE Downgrade activity**.

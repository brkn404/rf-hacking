# Pre-Engagement Anonymity Workflow

## Overview
This script automates the process of ensuring **anonymity** before conducting **OSINT or scanning activities**. It sets up a secure, anonymized environment by:
- **Randomizing MAC Address** to prevent tracking at the network level.
- **Starting & Monitoring Tor** to ensure traffic is anonymized.
- **Configuring ProxyChains & Torsocks** for routing tools like Nmap through Tor.
- **Verifying IP Rotation** to detect leaks before engagement.

## Installation & Setup
### 1️⃣ Install Required Packages
```sh
sudo apt update && sudo apt install tor macchanger proxychains4 torsocks -y
```

### 2️⃣ Configure Tor
- Open the configuration file:
  ```sh
  sudo nano /etc/tor/torrc
  ```
- Add or uncomment these lines:
  ```
  ControlPort 9051
  CookieAuthentication 0
  SocksPort 9050
  ```
- Restart Tor:
  ```sh
  sudo systemctl restart tor
  ```

### 3️⃣ Configure ProxyChains
- Edit the ProxyChains configuration:
  ```sh
  sudo nano /etc/proxychains.conf
  ```
- Add this at the end of the file:
  ```
  socks5 127.0.0.1 9050
  ```

### 4️⃣ Run the Script
```sh
sudo python3 pre_engagement_anon.py
```

## Workflow Phases
### **🔹 Phase 1: System Preparation & Isolation**
1. **MAC Address Randomization**
   - Prevents tracking via network logs.
   - Command used: `macchanger -r eth0`
2. **Tor Service Initialization**
   - Ensures Tor is running before any network activity.
   - Uses: `systemctl start tor`

### **🔹 Phase 2: Network Anonymization Setup**
3. **IP Rotation Monitoring**
   - Ensures Tor IP changes before engagement.
   - Fetches IP via `https://check.torproject.org`
4. **Tor Traffic Routing**
   - Ensures all tools use Tor (`proxychains4` & `torsocks`).

### **🔹 Phase 3: Anonymity Verification**
5. **Automated Leak Detection**
   - Runs multiple IP checks before engagement.
   - Warns if Tor IP is not rotating correctly.
6. **Failsafe Handling**
   - If IP is static, the script alerts the user.

### **🔹 Phase 4: Engagement Execution**
7. **Environment Validation**
   - If anonymity is verified, the system is ready for OSINT/scanning.
8. **Command Execution Through ProxyChains**
   - Example:
     ```sh
     proxychains4 nmap -sT -Pn example.com
     ```

## Usage Example
1. Run the script:
   ```sh
   sudo python3 pre_engagement_anon.py
   ```
2. Verify Tor IP:
   ```sh
   torsocks curl https://check.torproject.org/
   ```
3. Run OSINT tools through Tor:
   ```sh
   proxychains4 nmap -sT -Pn example.com
   ```

## Notes
- Ensure **Tor is properly configured** before running the script.
- If the **IP does not change**, restart Tor:
  ```sh
  sudo systemctl restart tor
  ```
- Always use `proxychains4` or `torsocks` to prevent leaks.

---
### **✅ This ensures anonymity before an engagement & warns about potential leaks! 🚀**


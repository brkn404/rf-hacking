"""
Tor IP Changer & Watchdog for OSINT & Scanning (Python)

This script changes your IP address using the Tor network at a specified interval and includes a watchdog
service to warn if the IP is not changing.

### Setup Instructions:
1. Install Tor:
   ```sh
   sudo apt update && sudo apt install tor -y
   ```
2. Start and Enable Tor:
   ```sh
   sudo systemctl start tor
   sudo systemctl enable tor
   ```
3. Configure Tor:
   - Open the config file:
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
4. Install `torsocks` & `proxychains` (for routing tools through Tor):
   ```sh
   sudo apt install torsocks proxychains4 -y
   ```
5. Configure ProxyChains:
   - Edit `/etc/proxychains.conf` and add this line at the end:
     ```
     socks5 127.0.0.1 9050
     ```
6. Run the Script:
   ```sh
   python3 tor_ip_changer.py
   ```
7. Use Tor for OSINT/Scanning:
   - Verify IP change:
     ```sh
     torsocks curl https://check.torproject.org/
     ```
   - Run Nmap through Tor:
     ```sh
     proxychains4 nmap -sT -Pn example.com
     ```

### Watchdog Feature:
- This script includes a **watchdog** that monitors whether the IP is changing correctly.
- If the IP remains the same for too long, it issues a warning.
"""

import time
import socket
import argparse
import requests

def get_current_ip():
    try:
        response = requests.get("https://check.torproject.org", proxies={"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"})
        return response.text.split("Your IP address appears to be ")[1].split(".")[0]
    except Exception as e:
        print(f"Error fetching current IP: {e}")
        return None

def change_ip():
    try:
        with socket.create_connection(("127.0.0.1", 9051)) as sock:
            sock.sendall(b"AUTHENTICATE \"\"\r\nSIGNAL NEWNYM\r\n")
            response = sock.recv(1024).decode()
            print(f"New IP requested through Tor. Response: {response.strip()}")
    except Exception as e:
        print(f"Error changing IP: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tor IP Changer & Watchdog for OSINT & Scanning")
    parser.add_argument("--interval", type=int, default=10, help="Time in seconds between IP changes (default: 10)")
    parser.add_argument("--watchdog", type=int, default=3, help="Number of consecutive failed IP changes before warning")
    args = parser.parse_args()
    
    last_ip = None
    failed_attempts = 0
    
    while True:
        current_ip = get_current_ip()
        if current_ip == last_ip:
            failed_attempts += 1
            if failed_attempts >= args.watchdog:
                print("⚠️ WARNING: IP has not changed for several cycles! Check Tor settings.")
        else:
            failed_attempts = 0
            print(f"Current Tor IP: {current_ip}")
        
        change_ip()
        last_ip = current_ip
        time.sleep(args.interval)  # Change IP at user-defined interval

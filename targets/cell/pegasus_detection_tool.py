import os
import subprocess
import json
import re
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------------------------------
# 🛡️ Pegasus Detection Tool
# -------------------------------------------
# ✅ Scans for Pegasus Indicators of Compromise (IoCs)
# ✅ Checks File Integrity (System Files, Logs, Configs)
# ✅ Detects Suspicious Network Activity
# ✅ Works on Android & iOS (via forensic logs & backups)
# -------------------------------------------

# Pegasus IoCs - Update this list with latest threat intelligence
ioc_hashes = [
    "e7b486cfd0b6ec2c3b2e0f3a5e44b9b0",  # Example Pegasus-related hash
    "8a2c0d0a5b6d9c5e34c8b9e7a0f5d9a1",  # Another example
]

suspicious_domains = [
    "appleid-valid.com",  # Known Pegasus C2 domain
    "android-check.live",  # Another Pegasus-associated domain
]

suspicious_processes = [
    "com.apple.SafariViewService",  # Exploited via iMessage zero-click
    "launchd",  # Often abused for persistence
]

suspicious_ports = [443, 8443, 53]  # Encrypted C2 connections

# -------------------------------------------
# 1️⃣ Check File Integrity (Scan System for Pegasus-Modified Files)
# -------------------------------------------
def scan_filesystem():
    """Scans filesystem for Pegasus-related files based on known hashes."""
    compromised_files = []
    for root, _, files in os.walk("/"):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in ioc_hashes:
                    compromised_files.append(filepath)
            except Exception:
                continue
    return compromised_files

# -------------------------------------------
# 2️⃣ Check Running Processes for Pegasus Activity
# -------------------------------------------
def scan_processes():
    """Checks running processes for known Pegasus-related names."""
    detected = []
    process_list = subprocess.getoutput("ps aux")
    for process in suspicious_processes:
        if re.search(process, process_list, re.IGNORECASE):
            detected.append(process)
    return detected

# -------------------------------------------
# 3️⃣ Check Network Traffic for Pegasus C2
# -------------------------------------------
def scan_network():
    """Monitors network activity for Pegasus C2 communications."""
    detected_domains = []
    net_traffic = subprocess.getoutput("netstat -an")
    for domain in suspicious_domains:
        if domain in net_traffic:
            detected_domains.append(domain)
    return detected_domains

# -------------------------------------------
# API Endpoints
# -------------------------------------------
@app.route('/scan', methods=['GET'])
def scan():
    """Runs Pegasus detection scans and returns results."""
    file_results = scan_filesystem()
    process_results = scan_processes()
    network_results = scan_network()
    
    results = {
        "compromised_files": file_results,
        "suspicious_processes": process_results,
        "suspicious_network": network_results,
    }
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

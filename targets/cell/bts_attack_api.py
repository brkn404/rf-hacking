import subprocess
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(filename="bts_attack_api_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# -------------------------------------------
# 📡 BTS Attack API
# -------------------------------------------
# ✅ Provides a centralized API for launching attack modules
# ✅ Supports Rogue BTS, Simjacker, Baseband, and OTA exploits
# ✅ Logs all attack execution requests
# ✅ Can be controlled remotely
# -------------------------------------------

# Available Attack Modules
ATTACK_MODULES = {
    "rogue_bts": "bts_rogue.py",
    "simjacker": "bts_simjacker.py",
    "baseband": "bts_baseband.py",
    "ota_exploit": "bts_ota_exploit.py"
}

@app.route('/start_attack/<attack_name>', methods=['POST'])
def start_attack(attack_name):
    """
    Runs a specific attack module.
    Example Request:
    curl -X POST http://<server-ip>:5007/start_attack/simjacker
    """
    if attack_name in ATTACK_MODULES:
        script_path = ATTACK_MODULES[attack_name]
        try:
            subprocess.Popen(["python3", script_path])
            logging.info(f"Started attack: {attack_name}")
            return jsonify({"status": "success", "message": f"Attack {attack_name} started"})
        except Exception as e:
            logging.error(f"Error starting attack {attack_name}: {str(e)}")
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid attack name"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)

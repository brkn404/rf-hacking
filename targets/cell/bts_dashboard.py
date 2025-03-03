import logging
from flask import Flask, render_template, jsonify

app = Flask(__name__)
logging.basicConfig(filename="bts_dashboard_logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# -------------------------------------------
# 🎛️ BTS Attack Control Panel
# -------------------------------------------
# ✅ Provides a web-based dashboard for managing attacks
# ✅ Displays real-time logs from attack modules
# ✅ Enables execution of Rogue BTS, Simjacker, Baseband, and OTA exploits
# ✅ Centralized control for all attack vectors
# -------------------------------------------

@app.route('/')
def dashboard():
    """
    Web UI Dashboard for BTS Attack Suite.
    Fetches logs and displays them in a browser-friendly format.
    """
    try:
        with open("bts_attack_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        return render_template("dashboard.html", logs=logs)
    except Exception as e:
        return f"Error loading logs: {str(e)}"

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    API endpoint to fetch logs for the web dashboard.
    Example Request:
    curl -X GET http://<server-ip>:5012/logs
    """
    try:
        with open("bts_attack_logs.txt", "r") as log_file:
            logs = log_file.readlines()
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)

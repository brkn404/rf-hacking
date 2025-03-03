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

# -------------------------------------------
# 📡 BTS Attack Suite - Modular Version
# -------------------------------------------
# ✅ Separated into independent scripts for better scalability
# ✅ Each module handles a specific attack vector
# ✅ All scripts communicate via API/Web UI
# ✅ Includes logging, attack management, and UI visualization
# ✅ Centralized BTS Controller to manage attack execution
# -------------------------------------------

# Modules
MODULES = {
    "rogue_bts": "bts_rogue.py",
    "attack_api": "bts_attack_api.py",
    "logger": "bts_logger.py",
    "simjacker": "bts_simjacker.py",
    "baseband": "bts_baseband.py",
    "ota_exploit": "bts_ota_exploit.py",
    "dashboard": "bts_dashboard.py"
}

@app.route('/')
def dashboard():
    """
    Web UI Dashboard for BTS Attack Suite.
    """
    with open("bts_attack_logs.txt", "r") as log_file:
        logs = log_file.readlines()
    return render_template("dashboard.html", logs=logs)

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Fetches attack logs from different attack modules.
    """
    with open("bts_attack_logs.txt", "r") as log_file:
        logs = log_file.readlines()
    return jsonify({"logs": logs})

@app.route('/run_module/<module_name>', methods=['POST'])
def run_module(module_name):
    """
    Runs a specific attack module by executing the respective script.
    Example: curl -X POST http://<server-ip>:5005/run_module/simjacker
    """
    if module_name in MODULES:
        script_path = MODULES[module_name]
        try:
            subprocess.Popen(["python3", script_path])
            logging.info(f"Started module: {module_name}")
            return jsonify({"status": "success", "message": f"Module {module_name} started"})
        except Exception as e:
            logging.error(f"Error starting module {module_name}: {str(e)}")
            return jsonify({"status": "error", "message": str(e)})
    else:
        return jsonify({"status": "error", "message": "Invalid module name"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

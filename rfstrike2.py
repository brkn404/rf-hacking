import tkinter as tk
from tkinter import ttk
import os
import subprocess
from PIL import Image, ImageTk

# -------------------------------------------
# RFStrike - Ultimate SDR Hacking Suite
# Optimized for 3.5" touchscreen display with tile-based UI
# -------------------------------------------

# Create main GUI window
root = tk.Tk()
root.title("RFStrike")
root.geometry("480x320")  # Optimized for 3.5" touchscreen
root.configure(bg="#121212")  # Dark cyber-themed background

# Apply style
tt_style = ttk.Style()
tt_style.configure("TButton", font=("Arial", 10, "bold"), padding=6, width=12)

def dummy_function(attack_name):
    status_label.config(text=f"Running: {attack_name}...", fg="#00FF00")
    root.update()

# Title Label
title_label = tk.Label(root, text="RFStrike", font=("Arial", 16, "bold"), fg="#00FF00", bg="#121212")
title_label.pack(pady=5)

# Load icons
icons = {
    "Wi-Fi Deauth": "wifi.png",
    "Bluetooth Hijack": "bluetooth.png",
    "Zigbee Sniffing": "zigbee.png",
    "GPS Spoofing": "gps.png",
    "RF Exfiltration": "rf_exfil.png",
    "Live SDR Scan": "sdr_scan.png",
    "Evil Twin AP": "evil_twin.png",
    "Covert RF Beacon": "rf_beacon.png"
}

buttons_frame = tk.Frame(root, bg="#121212")
buttons_frame.pack()

# Create a grid layout for better touchscreen usability
row_num = 0
col_num = 0
max_cols = 3  # Maximum number of columns per row

for attack, icon_file in icons.items():
    try:
        icon = Image.open(icon_file)
        icon = icon.resize((40, 40))  # Increase icon size for better visibility
        icon = ImageTk.PhotoImage(icon)
    except:
        icon = None
    
    btn = tk.Button(
        buttons_frame, text=attack, command=lambda a=attack: dummy_function(a), image=icon, compound=tk.TOP, 
        font=("Arial", 10, "bold"), fg="black", bg="#E0E0E0", relief=tk.RAISED, padx=6, pady=6, bd=2, width=12, height=6,
        highlightbackground="#00FF00", highlightthickness=2, borderwidth=3
    )
    btn.image = icon  # Prevent garbage collection
    btn.grid(row=row_num, column=col_num, padx=6, pady=6, sticky="nsew")
    
    col_num += 1
    if col_num >= max_cols:  # Adjust number of columns dynamically
        col_num = 0
        row_num += 1

# Status Label
status_label = tk.Label(root, text="Ready", font=("Arial", 12, "bold"), fg="#FFFFFF", bg="#121212")
status_label.pack(pady=5)

# USB Device Detection Panel
usb_label = tk.Label(root, text="Connected Devices:", font=("Arial", 10, "bold"), fg="#00FF00", bg="#121212")
usb_label.pack(pady=3)
usb_listbox = tk.Listbox(root, height=3, width=40, bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 9))
usb_listbox.pack(pady=3)

# Detect USB Devices
def update_usb_devices():
    usb_listbox.delete(0, tk.END)
    try:
        if os.uname().sysname == "Darwin":  # macOS
            devices = subprocess.check_output("system_profiler SPUSBDataType", shell=True).decode("utf-8").split("\n")
        else:  # Linux (Raspberry Pi)
            devices = subprocess.check_output("lsusb", shell=True).decode("utf-8").split("\n")
        for device in devices:
            if device.strip():
                usb_listbox.insert(tk.END, device)
    except subprocess.CalledProcessError:
        usb_listbox.insert(tk.END, "Error detecting USB devices")
    root.after(5000, update_usb_devices)  # Refresh every 5 seconds

update_usb_devices()

# Run GUI
root.mainloop()

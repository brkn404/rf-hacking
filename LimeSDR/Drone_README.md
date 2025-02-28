# Drone No-Fly Zone Bypass Tool

## Overview

The **Drone No-Fly Zone Bypass Tool** is designed to override UAV geofencing restrictions, allowing drones to operate in areas typically designated as no-fly zones. This is achieved through GPS spoofing, control signal hijacking, and disabling firmware-based geofencing.

## Features

- **GPS Spoofing:** Transmit counterfeit GPS signals to alter the drone's perceived location.
- **Control Signal Hijacking:** Intercept and manipulate the drone's command and control (C2) communications.
- **Geofencing Disablement:** Modify drone firmware to remove built-in no-fly zone limitations.
- **Automated Restricted Zone Detection:** Identify nearby restricted zones and provide real-time bypass options.

## Requirements

- **Hardware:**
  - LimeSDR Mini or HackRF One
  - 5W-10W RF Power Amplifier (2.4 GHz and/or 5.8 GHz)
  - Directional Panel or Yagi Antenna

- **Software:**
  - Python 3.x
  - SoapySDR
  - GNU Radio
  - gps-sdr-sim
  - RFCrack

## Setup Instructions

1. **Hardware Assembly:**
   - Connect the SDR (LimeSDR Mini or HackRF One) to your computer via USB.
   - Attach the RF Power Amplifier to the SDR's transmit (TX) port.
   - Connect the directional antenna to the output of the RF Power Amplifier.
   - Ensure all connections are secure and appropriately rated for the frequencies in use.

2. **Software Installation:**
   - Install the required software packages:
     ```bash
     sudo apt-get update
     sudo apt-get install python3 python3-pip gnuradio
     pip3 install SoapySDR gps-sdr-sim RFCrack
     ```

3. **Configuration:**
   - Clone or download the `drone_no_fly_bypass.py` script to your local machine.
   - Ensure the script has executable permissions:
     ```bash
     chmod +x drone_no_fly_bypass.py
     ```
   - Modify any script parameters as needed to suit your specific use case.

## Usage

1. **Detect and Alert Restricted Zones:**
   ```bash
   python3 drone_no_fly_bypass.py --detect-zones

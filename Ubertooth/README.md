Ubertooth BLE Hacking Toolkit

This repository contains offensive & defensive BLE security tools designed specifically for use with the Ubertooth One. Ubertooth is a powerful open-source platform for Bluetooth sniffing, active attacks, and analysis.
What is Ubertooth One?

Ubertooth One is a 2.4 GHz Bluetooth sniffer and transceiver that supports both Classic Bluetooth (BR/EDR) and Bluetooth Low Energy (BLE). Unlike most consumer BLE adapters, Ubertooth can operate in promiscuous mode, meaning it can capture and analyze raw BLE traffic, including encrypted packets.
Capabilities of Ubertooth One
Feature	Description
✅ Promiscuous Mode	Captures all BLE traffic, including devices not directly paired with your system.
✅ BLE Packet Sniffing	Intercept and decode BLE advertisements, connections, and encrypted traffic.
✅ Real-Time BLE MITM Attacks	Modify and forward BLE packets in real-time for Man-in-the-Middle attacks.
✅ BLE Deauthentication & Jamming	Disrupt BLE connections by sending malformed packets and advertising floods.
✅ BLE Device Cloning & Impersonation	Replay BLE advertisements to spoof trusted devices (e.g., BLE door badges, fitness trackers).
✅ BLE Fuzzing & Exploitation	Brute-force BLE characteristics and discover hidden commands.
✅ Advanced BLE Hidden Service Scanning	Find stealth-mode AirTags, Tile trackers, and BLE malware beacons.
✅ BLE Packet Injection & Replay	Modify sensor data, authentication keys, and control signals for targeted attacks.
✅ Bluetooth Classic (BT BR/EDR) Sniffing	Capture and analyze Bluetooth Classic traffic (not just BLE).
✅ Custom BLE Firmware & Development	Modify Ubertooth's firmware for custom BLE hacking tools.
Use Cases for Ubertooth One

Ubertooth is widely used in cybersecurity research, penetration testing, and IoT security analysis. Below are some common real-world attack scenarios:
1️⃣ Sniffing and Capturing BLE Traffic

    Intercept BLE communications between devices and log all activity.
    Analyze unencrypted data in Wireshark for vulnerabilities.
    Monitor BLE beacons for tracking and surveillance applications.

2️⃣ BLE MITM Attacks (Man-in-the-Middle)

    Modify BLE packets on-the-fly.
    Intercept authentication and pairing requests.
    Inject malicious data into BLE-enabled applications.

3️⃣ BLE Deauthentication & Jamming

    Disrupt BLE connections to force re-authentication.
    Jamming BLE advertisements to prevent new device pairings.
    Target specific BLE devices for selective interference.

4️⃣ BLE Device Cloning & Impersonation

    Replay stolen BLE advertisements to mimic a trusted device.
    Spoof smart locks, access badges, and fitness trackers.
    Bypass security checkpoints and authentication gates.

5️⃣ BLE Fuzzing & Exploitation

    Brute-force BLE characteristics to find hidden commands.
    Crash or exploit vulnerable BLE devices.
    Modify authentication parameters to bypass security.

6️⃣ Bluetooth Classic (BT BR/EDR) Attacks

    Sniff Bluetooth keyboard & mouse traffic.
    Analyze audio device communications.
    Hijack Bluetooth connections for injection attacks.

Planned Scripts for Ubertooth One

Now that we've outlined Ubertooth's capabilities & use cases, here’s the roadmap for Ubertooth scripts:
Script	Description
ubertooth_sniffer.py	Sniff BLE & Bluetooth Classic traffic and save to PCAP format for Wireshark analysis.
ubertooth_mitm.py	Perform a Man-in-the-Middle (MITM) attack on BLE connections. Modify and relay packets in real-time.
ubertooth_jamming.py	Deauthenticate and jam BLE devices by sending malformed or flood packets.
ubertooth_cloner.py	Clone and impersonate BLE devices by replaying captured advertisement packets.
ubertooth_fuzzer.py	Fuzz BLE characteristics to find hidden services and exploit vulnerable devices.
ubertooth_bt_classic.py	Sniff and analyze Bluetooth Classic (BR/EDR) traffic. Can be used for keyboard, mouse, and audio sniffing.




Ubertooth Bluetooth Attack Toolkit
Overview

This repository contains a collection of Ubertooth-based Bluetooth attack scripts, including tools for MITM attacks, jamming, device impersonation, fuzzing, and more. These scripts are designed for Bluetooth Classic & BLE security research, penetration testing, and red teaming.

    ⚠ Disclaimer: These scripts are for educational & authorized security testing purposes only. Unauthorized use against systems you do not own or have explicit permission to test is illegal.

Setup & Installation
Install Required Dependencies

    Install Ubertooth tools:

sudo apt install ubertooth ubertooth-btle hcitool bluez gatttool btmgmt

Install required Python libraries:

    pip install -r requirements.txt

Available Ubertooth Scripts
Bluetooth Classic & BLE Sniffing

    ubertooth_bt_classic.py – Sniffs Bluetooth Classic (BR/EDR) traffic, used for keyboard, mouse, and audio sniffing.
    ubertooth_ble_dos.py – Performs BLE Denial-of-Service (DoS) attacks by flooding connections.
    ubertooth_rssi_tracking.py – Uses RSSI data to estimate Bluetooth device location and track movement.
    ubertooth_live_monitor.py – Real-time Bluetooth traffic dashboard for monitoring active devices.
    ubertooth_sniffer.txt – Configuration file for Ubertooth sniffing.

Man-in-the-Middle (MITM) Attacks

    ble_mitm_ubertooth.py – BLE MITM attack that captures & modifies Bluetooth traffic.
    ubertooth_bt_classic_mitm.py – MITM attack targeting Bluetooth Classic devices.
    ubertooth_persistent_mitm.py – Creates a persistent MITM channel between Bluetooth devices for long-term traffic interception.

Device Spoofing & Cloning

    ubertooth_cloner.py – Clones and impersonates BLE devices by replaying captured advertisement packets.
    ubertooth_beacon_spoof.py – Spoofs BLE beacons (AirTags, Tile, IoT sensors) for impersonation attacks.
    ubertooth_airtag_tracker.py – Detects & tracks hidden BLE AirTags & smart trackers used for stalking.
    ubertooth_hid_hijack.py – Hijacks Bluetooth HID devices (keyboards, mice) and takes control.
    ubertooth_keystroke_inject.py – Injects keystrokes into vulnerable Bluetooth keyboards using captured HID packets.

Denial-of-Service & Jamming

    ble_jamming_attack.py – BLE jamming & deauthentication attack against Bluetooth Low Energy devices.
    ubertooth_mass_deauth.py – Jams and deauths all Bluetooth Classic & BLE devices in range for maximum disruption.
    ubertooth_classic_downgrade.py – Forces Bluetooth Classic connections to downgrade encryption, making them easier to MITM.
    ubertooth_ble_dos.py – Floods BLE channels to deny service to devices.

Bluetooth Fuzzing & Exploits

    ubertooth_fuzzer.py – Performs Bluetooth fuzzing to discover vulnerabilities in Bluetooth stacks.
    ubertooth_l2cap_inject.py – Injects malicious L2CAP packets to exploit Bluetooth protocol weaknesses.
    ubertooth_pairing_hijack.py – Intercepts Bluetooth pairing requests & exploits weak authentication.
    ubertooth_smart_lock_bypass.py – Bypasses Bluetooth-based smart locks using brute-force or replay attacks.
    ubertooth_iot_exploit.py – Targets IoT devices with insecure BLE implementations (smart thermostats, security systems, etc.).
    ubertooth_replay.py – Replays captured Bluetooth packets to replicate device behavior.

Advanced Attacks & Enhancements

    ubertooth_adv_hopping.py – Implements adaptive frequency hopping to improve packet capture efficiency across changing channels.
    ubertooth_sdr_bridge.py – Bridges Ubertooth with SDR devices (HackRF, LimeSDR) for expanded Bluetooth analysis & attack capabilities.
    ubertooth_auto_pwn.py – Automates scanning, MITM, pairing hijack, and deauth into one script for full attack automation.
    ubertooth_stealth_sniff.py – Passive sniffing mode that reduces detection risk by adjusting scan timing and packet injection.

Usage Examples
Sniff BLE Devices

python ubertooth_bt_classic.py --scan

Perform a BLE MITM Attack

python ble_mitm_ubertooth.py --target AA:BB:CC:DD:EE:FF

Jam All BLE Devices

python ble_jamming_attack.py --jam-all

Bypass a Bluetooth Smart Lock

python ubertooth_smart_lock_bypass.py --target AA:BB:CC:DD:EE:FF --replay unlock_packet.bin

Track a Suspicious AirTag

python ubertooth_airtag_tracker.py --monitor

Legal Disclaimer

This repository is strictly for educational and authorized penetration testing purposes only.
Do not use these tools against networks, systems, or devices you do not own or have explicit permission to test.
Unauthorized access to networks and devices is illegal and punishable by law.

    Use responsibly. 🚀

Credits

Developed & maintained for Bluetooth security research, red teaming, & penetration testing.

If you find this repository useful, consider contributing or reporting issues! 🚀

This README.md file is now fully formatted & ready to be dropped into your project. Let me know if you need further modifications! 🚀



import argparse
import subprocess
import time
import os
import wave
import struct

"""
Ubertooth Bluetooth Audio Sniffer

Features:
    - Sniffs Bluetooth Classic (BR/EDR) audio traffic.
    - Captures and logs Bluetooth SCO (Synchronous Connection-Oriented) packets.
    - Decodes Bluetooth audio packets into playable WAV files.
    - Supports live Bluetooth audio reconstruction & playback.
    - Filters packets by target MAC address.
    - Logs detected Bluetooth audio activity.

Requirements:
    - Ubertooth One
    - Install Ubertooth utilities: sudo apt install ubertooth ubertooth-btle
    - Install Sox for playback: sudo apt install sox

Usage:
    - Scan for Bluetooth Classic audio devices:
      python ubertooth_audio_sniffer.py --scan
    - Capture and log Bluetooth audio traffic:
      python ubertooth_audio_sniffer.py --capture --log bt_audio.pcap
    - Filter packets for a specific Bluetooth audio device (e.g., headset MAC address):
      python ubertooth_audio_sniffer.py --capture --target AA:BB:CC:DD:EE:FF --log bt_audio_filtered.pcap
    - Decode Bluetooth audio packets into a playable WAV file:
      python ubertooth_audio_sniffer.py --decode --input bt_audio.pcap --output extracted_audio.wav
    - Live audio reconstruction & playback:
      python ubertooth_audio_sniffer.py --live-decode
"""

def scan_bluetooth_audio_devices():
    """Scans for Bluetooth Classic devices that support audio."""
    print("[INFO] Scanning for Bluetooth Classic audio devices...")

    try:
        output = subprocess.check_output(["ubertooth-rx", "-s"])
        devices = output.decode("utf-8").split("\n")

        for line in devices:
            if "Audio" in line or "SCO" in line:
                print(f"[DETECTED] Bluetooth Audio Device: {line.strip()}")

    except Exception as e:
        print(f"[ERROR] Failed to scan for Bluetooth audio devices: {e}")

def capture_audio_traffic(log_file, target_mac=None):
    """Captures Bluetooth Classic audio traffic and logs it to a PCAP file."""
    print(f"[INFO] Capturing Bluetooth Classic audio traffic (Logging to {log_file})...")

    try:
        cmd = ["ubertooth-rx", "-f", "-o", log_file]
        if target_mac:
            cmd.extend(["-m", target_mac])

        subprocess.run(cmd)
        print(f"[SUCCESS] Bluetooth audio packets saved to {log_file}")

    except Exception as e:
        print(f"[ERROR] Failed to capture Bluetooth audio traffic: {e}")

def decode_bluetooth_audio(input_pcap, output_wav):
    """Decodes Bluetooth audio packets from PCAP and reconstructs them into a WAV file."""
    print(f"[INFO] Decoding Bluetooth audio packets from {input_pcap}...")

    try:
        # Extract raw SCO data
        sco_packets = []
        output = subprocess.check_output(["ubertooth-rx", "-r", input_pcap])
        packets = output.decode("utf-8").split("\n")

        for line in packets:
            if "SCO" in line:
                raw_data = line.split("SCO:")[1].strip()
                sco_packets.append(bytes.fromhex(raw_data))

        if not sco_packets:
            print("[WARNING] No SCO audio packets found.")
            return

        # Save as WAV file
        with wave.open(output_wav, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(8000)  # Standard Bluetooth SCO rate

            for packet in sco_packets:
                for i in range(0, len(packet), 2):
                    sample = struct.unpack("<h", packet[i:i+2])[0]
                    wav_file.writeframes(struct.pack("<h", sample))

        print(f"[SUCCESS] Decoded Bluetooth audio saved to {output_wav}")
        print("[INFO] Playing extracted audio...")
        os.system(f"play {output_wav}")  # Play the extracted audio

    except Exception as e:
        print(f"[ERROR] Failed to decode Bluetooth audio: {e}")

def live_decode_audio():
    """Attempts to decode Bluetooth audio traffic in real-time and play it back."""
    print("[INFO] Attempting to decode Bluetooth audio traffic in real-time...")

    try:
        process = subprocess.Popen(["ubertooth-rx", "-f"], stdout=subprocess.PIPE, text=True)

        with wave.open("live_audio.wav", "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(8000)

            for line in iter(process.stdout.readline, ""):
                if "SCO" in line:
                    raw_data = line.split("SCO:")[1].strip()
                    audio_packet = bytes.fromhex(raw_data)

                    for i in range(0, len(audio_packet), 2):
                        sample = struct.unpack("<h", audio_packet[i:i+2])[0]
                        wav_file.writeframes(struct.pack("<h", sample))

        print("[SUCCESS] Live Bluetooth audio captured. Playing now...")
        os.system("play live_audio.wav")

    except Exception as e:
        print(f"[ERROR] Failed to decode live Bluetooth audio: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubertooth Bluetooth Audio Sniffer")
    parser.add_argument("--scan", action="store_true", help="Scan for Bluetooth Classic audio devices")
    parser.add_argument("--capture", action="store_true", help="Capture Bluetooth audio traffic")
    parser.add_argument("--log", type=str, help="Log file for captured audio packets")
    parser.add_argument("--target", type=str, help="Filter packets by target MAC address")
    parser.add_argument("--decode", action="store_true", help="Decode captured Bluetooth audio into WAV format")
    parser.add_argument("--input", type=str, help="Input PCAP file for audio decoding")
    parser.add_argument("--output", type=str, help="Output WAV file for decoded audio")
    parser.add_argument("--live-decode", action="store_true", help="Attempt to decode and play Bluetooth audio in real-time")

    args = parser.parse_args()

    if args.scan:
        scan_bluetooth_audio_devices()
    elif args.capture and args.log:
        capture_audio_traffic(args.log, args.target)
    elif args.decode and args.input and args.output:
        decode_bluetooth_audio(args.input, args.output)
    elif args.live_decode:
        live_decode_audio()
    else:
        print("[ERROR] No valid mode selected! Use --scan, --capture with --log, --decode with --input and --output, or --live-decode.")

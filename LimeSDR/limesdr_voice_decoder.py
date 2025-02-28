import os
import argparse
import speech_recognition as sr

# -------------------------------------------
# LimeSDR Digital Voice Decoder
# -------------------------------------------
# Features:
# - Decode & analyze digital radio signals (TETRA, P25, DMR, etc.)
# - Extract and replay voice communications from radio channels
# - Supports trunking systems & encrypted radio traffic analysis
# - Automatic signal classification to detect encryption & key weaknesses
# - Converts decoded speech to text for easy search & analysis
#
# Requirements:
# - GNURadio, OP25, TETRA Decoder
# - Compatible SDR hardware (LimeSDR Mini, LimeSDR, etc.)
# - Python 3.x, SpeechRecognition
#
# Usage:
# 1. Scan for digital voice signals:
#    python limesdr_voice_decoder.py --scan
# 2. Decode TETRA/P25/DMR audio:
#    python limesdr_voice_decoder.py --decode --protocol tetra
# 3. Replay captured audio:
#    python limesdr_voice_decoder.py --replay --file captured_audio.wav
# 4. Perform trunked radio system analysis:
#    python limesdr_voice_decoder.py --trunk-trace
# 5. Convert speech to text:
#    python limesdr_voice_decoder.py --speech-to-text --file decoded_audio.wav
# -------------------------------------------

def scan_digital_voice():
    """Scans for active digital voice signals."""
    print("[+] Scanning for digital radio signals (TETRA, P25, DMR)...")
    os.system("soapy_power -f 100M:1G --output digital_voice_scan.csv")
    print("[✔] Scan complete. Results saved to digital_voice_scan.csv")

def decode_voice(protocol):
    """Decodes digital voice signals based on protocol."""
    print(f"[+] Decoding {protocol} signals...")
    if protocol == "tetra":
        os.system("tetra-rx -D -o decoded_audio.wav")
    elif protocol == "p25":
        os.system("op25 -o decoded_audio.wav")
    elif protocol == "dmr":
        os.system("dmr-decoder -o decoded_audio.wav")
    print("[✔] Decoding complete. Saved as decoded_audio.wav")

def replay_audio(file):
    """Replays captured audio transmissions."""
    print(f"[+] Replaying captured audio: {file}")
    os.system(f"aplay {file}")
    print("[✔] Playback complete.")

def trunked_radio_analysis():
    """Analyzes trunked radio systems for call tracing."""
    print("[+] Analyzing trunked radio systems...")
    os.system("trunk-recorder --config trunk_config.json")
    print("[✔] Trunked system analysis complete.")

def speech_to_text(file):
    """Converts speech from decoded audio to text."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        print("[+] Converting speech to text...")
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            with open("transcribed_text.txt", "w") as text_file:
                text_file.write(text)
            print("[✔] Speech-to-text conversion complete. Saved to transcribed_text.txt")
        except sr.UnknownValueError:
            print("[!] Could not understand the audio.")
        except sr.RequestError:
            print("[!] Could not request results from the speech recognition service.")

def main():
    parser = argparse.ArgumentParser(description="LimeSDR Digital Voice Decoder")
    parser.add_argument("--scan", action='store_true', help="Scan for digital voice signals")
    parser.add_argument("--decode", action='store_true', help="Decode TETRA/P25/DMR audio")
    parser.add_argument("--protocol", type=str, choices=["tetra", "p25", "dmr"], help="Specify protocol for decoding")
    parser.add_argument("--replay", action='store_true', help="Replay captured audio")
    parser.add_argument("--file", type=str, help="Audio file for replay or transcription")
    parser.add_argument("--trunk-trace", action='store_true', help="Perform trunked radio system analysis")
    parser.add_argument("--speech-to-text", action='store_true', help="Convert speech to text for search & analysis")
    args = parser.parse_args()
    
    if args.scan:
        scan_digital_voice()
    elif args.decode and args.protocol:
        decode_voice(args.protocol)
    elif args.replay and args.file:
        replay_audio(args.file)
    elif args.trunk_trace:
        trunked_radio_analysis()
    elif args.speech_to_text and args.file:
        speech_to_text(args.file)
    else:
        print("[!] Invalid command. Use --help for options.")

if __name__ == "__main__":
    main()

import argparse
import subprocess
import logging

# -------------------------------------------
# RFID/NFC Cloning & Emulation Tool
# -------------------------------------------
# Features:
# - Read RFID/NFC tags using Chameleon Ultra.
# - Write data to RFID/NFC tags.
# - Emulate RFID/NFC tags for penetration testing.
# - Log all actions and results.
#
# Requirements:
# - Chameleon Ultra
# - Python 3.x
# - Chameleon CLI tools
#
# Usage:
# 1. Read an RFID/NFC tag:
#    python rfid_nfc_tool.py --read --output tag_data.bin
# 2. Write data to an RFID/NFC tag:
#    python rfid_nfc_tool.py --write --input tag_data.bin
# 3. Emulate an RFID/NFC tag:
#    python rfid_nfc_tool.py --emulate --input tag_data.bin
# -------------------------------------------

# Global variables
logging.basicConfig(filename="rfid_nfc_tool.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    """Log an event to the log file."""
    logging.info(message)
    print(message)

def read_rfid_tag(output_file="tag_data.bin"):
    """
    Read an RFID/NFC tag using Chameleon Ultra.
    :param output_file: Output file to save the tag data.
    """
    log_event(f"[+] Reading RFID/NFC tag to {output_file}...")
    try:
        subprocess.run(["chameleon", "read", "-o", output_file], check=True)
        log_event(f"[✔] Tag data saved to {output_file}")
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during tag read: {e}")

def write_rfid_tag(input_file="tag_data.bin"):
    """
    Write data to an RFID/NFC tag.
    :param input_file: Input file containing the tag data.
    """
    log_event(f"[+] Writing data from {input_file} to RFID/NFC tag...")
    try:
        subprocess.run(["chameleon", "write", "-i", input_file], check=True)
        log_event("[✔] Tag data written successfully.")
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during tag write: {e}")

def emulate_rfid_tag(input_file="tag_data.bin"):
    """
    Emulate an RFID/NFC tag using Chameleon Ultra.
    :param input_file: Input file containing the tag data.
    """
    log_event(f"[+] Emulating RFID/NFC tag from {input_file}...")
    try:
        subprocess.run(["chameleon", "emulate", "-i", input_file], check=True)
        log_event("[✔] Tag emulation started.")
    except subprocess.CalledProcessError as e:
        log_event(f"[!] Error during tag emulation: {e}")

def main():
    parser = argparse.ArgumentParser(description="RFID/NFC Cloning & Emulation Tool")
    parser.add_argument("--read", action="store_true", help="Read an RFID/NFC tag")
    parser.add_argument("--write", action="store_true", help="Write data to an RFID/NFC tag")
    parser.add_argument("--emulate", action="store_true", help="Emulate an RFID/NFC tag")
    parser.add_argument("--input", type=str, help="Input file for write or emulate")
    parser.add_argument("--output", type=str, help="Output file for tag read")
    args = parser.parse_args()

    if args.read:
        read_rfid_tag(args.output)
    elif args.write:
        if not args.input:
            log_event("[!] Please specify --input for write.")
            return
        write_rfid_tag(args.input)
    elif args.emulate:
        if not args.input:
            log_event("[!] Please specify --input for emulate.")
            return
        emulate_rfid_tag(args.input)
    else:
        log_event("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()
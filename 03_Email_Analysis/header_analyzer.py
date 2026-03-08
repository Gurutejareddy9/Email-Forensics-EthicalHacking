# EDUCATIONAL USE ONLY
# ============================================================
# header_analyzer.py
#
# PURPOSE: Parse and analyse the headers of a .eml file to
#          identify email spoofing indicators.
#
# WHAT IT DOES:
#   1. Reads sample_email.eml using Python's built-in email library
#   2. Prints all headers in a clean, readable format
#   3. Compares the 'From' display domain with the Reply-To domain
#   4. Checks the X-Originating-IP header for suspicious IPs
#   5. Flags any spoofing indicators found
#
# LIBRARY USED: Python standard library only (email module)
# ============================================================

import email
import os
import re
import sys


# ── Helpers ──────────────────────────────────────────────────

def extract_domain(address):
    """
    Extract the domain part from an email address like:
        'James Hartwell <j.hartwell@techcorp.co.uk>'  →  'techcorp.co.uk'
        'ceo@techcorp-ltd.xyz'                          →  'techcorp-ltd.xyz'
    """
    match = re.search(r"@([\w.\-]+)", address)
    if match:
        return match.group(1).lower()
    return None


def is_private_ip(ip_str):
    """
    Returns True if the IP address looks like a private/reserved range.
    Private ranges: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
    """
    private_patterns = [
        r"^10\.",
        r"^172\.(1[6-9]|2\d|3[01])\.",
        r"^192\.168\.",
    ]
    for pattern in private_patterns:
        if re.match(pattern, ip_str):
            return True
    return False


# ── Main Analysis ─────────────────────────────────────────────

def analyse_headers(filepath):
    """
    Load an .eml file, print all headers, and flag spoofing indicators.
    """
    separator = "=" * 65

    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return

    # Read and parse the email file
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw_email = f.read()

    msg = email.message_from_string(raw_email)

    # ── Section 1: Print all headers ────────────────────────
    print(separator)
    print("  EMAIL HEADER ANALYSIS")
    print(f"  File: {os.path.abspath(filepath)}")
    print(separator)
    print("\n[+] ALL HEADERS\n")
    for header, value in msg.items():
        print(f"  {header:<22}: {value}")

    # ── Section 2: Extract key fields for analysis ───────────
    print("\n" + separator)
    print("[+] KEY FIELD ANALYSIS")
    print(separator)

    from_header  = msg.get("From", "")
    reply_to     = msg.get("Reply-To", "")
    message_id   = msg.get("Message-ID", "")
    originating_ip = msg.get("X-Originating-IP", "")
    received_headers = msg.get_all("Received") or []

    print(f"\n  From         : {from_header}")
    print(f"  Reply-To     : {reply_to if reply_to else '(not set)'}")
    print(f"  Message-ID   : {message_id}")
    print(f"  Orig. IP     : {originating_ip if originating_ip else '(not set)'}")

    # ── Section 3: Received chain ───────────────────────────
    print(f"\n  Received headers ({len(received_headers)} hop(s)):")
    for i, rcv in enumerate(received_headers, start=1):
        print(f"    Hop {i}: {rcv.strip()}")

    # ── Section 4: Spoofing indicators ──────────────────────
    print("\n" + separator)
    print("[!] SPOOFING INDICATOR CHECK")
    print(separator)

    indicators_found = []

    # Check 1: From domain vs Reply-To domain mismatch
    from_domain    = extract_domain(from_header)
    reply_to_domain = extract_domain(reply_to) if reply_to else None

    print(f"\n  Check 1 — From domain    : {from_domain or 'unknown'}")
    print(f"            Reply-To domain : {reply_to_domain or '(not set)'}")

    if reply_to_domain and from_domain and reply_to_domain != from_domain:
        flag = f"MISMATCH — From domain '{from_domain}' ≠ Reply-To domain '{reply_to_domain}'"
        indicators_found.append(flag)
        print(f"  [!] {flag}")
    else:
        print("  [OK] From and Reply-To domains match (or Reply-To not set)")

    # Check 2: Message-ID domain vs From domain
    msgid_domain = extract_domain(message_id)
    print(f"\n  Check 2 — Message-ID domain : {msgid_domain or 'unknown'}")
    if msgid_domain and from_domain and msgid_domain != from_domain:
        flag = f"MISMATCH — Message-ID domain '{msgid_domain}' ≠ From domain '{from_domain}'"
        indicators_found.append(flag)
        print(f"  [!] {flag}")
    else:
        print("  [OK] Message-ID domain matches From domain")

    # Check 3: X-Originating-IP analysis
    print(f"\n  Check 3 — X-Originating-IP : {originating_ip or '(not present)'}")
    if originating_ip:
        ip_clean = originating_ip.strip()
        if is_private_ip(ip_clean):
            flag = f"SUSPICIOUS — Originating IP '{ip_clean}' is in a private range; may be forged or internal relay"
            indicators_found.append(flag)
            print(f"  [!] {flag}")
        else:
            print(f"  [i] IP '{ip_clean}' appears to be a public address — cross-check with threat intel")
    else:
        print("  [i] X-Originating-IP header not present")

    # Check 4: Lookalike domains in any header
    all_header_text = " ".join(str(v) for v in msg.values())
    lookalike_pattern = re.compile(r"techcorp-ltd\.xyz", re.IGNORECASE)
    if lookalike_pattern.search(all_header_text):
        flag = "Lookalike domain 'techcorp-ltd.xyz' found in headers — likely impersonation"
        indicators_found.append(flag)
        print(f"\n  [!] {flag}")

    # ── Section 5: Summary ──────────────────────────────────
    print("\n" + separator)
    print("[+] SUMMARY")
    print(separator)
    if indicators_found:
        print(f"\n  {len(indicators_found)} spoofing indicator(s) detected:\n")
        for idx, indicator in enumerate(indicators_found, start=1):
            print(f"  {idx}. {indicator}")
        print("\n  VERDICT: This email exhibits strong signs of SPOOFING.")
    else:
        print("\n  No spoofing indicators detected.")
        print("  VERDICT: Headers appear consistent (further analysis still recommended).")

    print(separator)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        eml_path = sys.argv[1]
    else:
        # Default to sample_email.eml in the Evidence Collection folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        eml_path = os.path.join(
            script_dir, "..", "02_Evidence_Collection", "sample_email.eml"
        )

    analyse_headers(eml_path)

# EDUCATIONAL USE ONLY
# ============================================================
# url_extractor.py
#
# PURPOSE: Extract all URLs from the body of a .eml file and
#          flag suspicious ones based on common phishing
#          indicators.
#
# PHISHING URL INDICATORS CHECKED:
#   1. Raw IP address instead of a domain name
#   2. Unusual / suspicious TLDs (.xyz, .top, .tk, .pw, etc.)
#   3. Keywords often used in credential-harvesting pages
#      (login, verify, account, secure, update, confirm)
#   4. No HTTPS (plain HTTP)
#   5. Lookalike domain patterns
#
# LIBRARY USED: Python standard library only (re, email)
# ============================================================

import email
import os
import re
import sys


# ── Phishing indicator patterns ──────────────────────────────

# Matches raw IPv4 addresses in URLs, e.g. http://192.168.100.200/
IP_IN_URL_PATTERN = re.compile(
    r"https?://(\d{1,3}\.){3}\d{1,3}(:\d+)?(/[^\s]*)?"
)

# Suspicious TLDs commonly abused by phishers
SUSPICIOUS_TLDS = {".xyz", ".top", ".tk", ".pw", ".ml", ".ga", ".cf", ".gq", ".click", ".work"}

# Keywords in the URL path/query that suggest credential harvesting
PHISHING_KEYWORDS = {"login", "verify", "account", "secure", "update", "confirm", "signin", "auth"}

# General URL extraction regex (covers http, https)
URL_PATTERN = re.compile(
    r"https?://[^\s\"'<>()\\]+"
)


# ── Helpers ──────────────────────────────────────────────────

def get_email_body(filepath):
    """
    Reads the .eml file and returns the plain-text body as a string.
    """
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    msg = email.message_from_string(raw)

    # Walk through all MIME parts to find text/plain
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode("utf-8", errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode("utf-8", errors="replace")
        # Fallback: return raw payload as string (not base64 encoded)
        return msg.get_payload()

    return ""


def assess_url(url):
    """
    Analyse a single URL and return a list of suspicion reasons.

    Returns:
        list[str]: Reasons the URL is considered suspicious (empty = clean).
    """
    reasons = []

    # Check 1: Raw IP address
    if IP_IN_URL_PATTERN.match(url):
        reasons.append("Contains raw IP address instead of domain name")

    # Check 2: HTTP (not HTTPS)
    if url.startswith("http://"):
        reasons.append("Uses plain HTTP (no encryption)")

    # Check 3: Suspicious TLD
    # Extract the domain portion (between :// and the next / or end)
    domain_match = re.search(r"https?://([^\s/]+)", url)
    if domain_match:
        domain = domain_match.group(1).lower()
        # Remove port number if present
        domain_no_port = domain.split(":")[0]
        # Check each suspicious TLD suffix
        for tld in SUSPICIOUS_TLDS:
            if domain_no_port.endswith(tld):
                reasons.append(f"Suspicious TLD detected: '{tld}'")
                break

    # Check 4: Phishing keywords in the URL
    url_lower = url.lower()
    for keyword in PHISHING_KEYWORDS:
        if keyword in url_lower:
            reasons.append(f"Phishing keyword in URL: '{keyword}'")
            break  # Only report first match to keep output concise

    return reasons


# ── Main ─────────────────────────────────────────────────────

def extract_and_analyse_urls(filepath):
    """
    Main function: extract URLs from the email body and print analysis.
    """
    separator = "=" * 65

    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return

    body = get_email_body(filepath)

    if not body:
        print("[WARNING] Could not extract email body.")
        return

    urls = URL_PATTERN.findall(body)

    print(separator)
    print("  URL EXTRACTOR — PHISHING LINK ANALYSIS")
    print(f"  File: {os.path.abspath(filepath)}")
    print(separator)

    if not urls:
        print("\n  No URLs found in the email body.")
        print(separator)
        return

    print(f"\n  {len(urls)} URL(s) found in the email body:\n")

    suspicious_count = 0

    for i, url in enumerate(urls, start=1):
        reasons = assess_url(url)
        status = "SUSPICIOUS" if reasons else "CLEAN"

        if reasons:
            suspicious_count += 1
            print(f"  [{i}] {url}")
            print(f"       Status  : *** {status} ***")
            for reason in reasons:
                print(f"       Reason  : {reason}")
        else:
            print(f"  [{i}] {url}")
            print(f"       Status  : {status}")

        print()

    print(separator)
    print(f"[+] SUMMARY: {suspicious_count} of {len(urls)} URL(s) flagged as SUSPICIOUS")
    if suspicious_count > 0:
        print("    Recommendation: Do NOT click these links.")
        print("    Submit to VirusTotal or a sandbox for further analysis.")
    print(separator)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        eml_path = sys.argv[1]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        eml_path = os.path.join(
            script_dir, "..", "02_Evidence_Collection", "sample_email.eml"
        )

    extract_and_analyse_urls(eml_path)

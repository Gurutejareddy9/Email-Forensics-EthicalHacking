# EDUCATIONAL USE ONLY
# ============================================================
# attachment_scanner.py
#
# PURPOSE: Simulate scanning an email attachment for threats.
#
# WHAT IT DOES:
#   1. Checks the file extension against a list of dangerous
#      extensions commonly used in malware delivery.
#   2. Calculates the MD5 and SHA-256 hashes of the file
#      (for comparison against threat intelligence databases).
#   3. Prints a threat assessment report.
#
# NOTE: This is a SIMULATION. In a real investigation you
#       would cross-check hashes against databases like
#       VirusTotal, MalwareBazaar, or NSRL.
#
# LIBRARY USED: Python standard library only (hashlib, os)
# ============================================================

import hashlib
import os
import sys


# ── Configuration ─────────────────────────────────────────────

# File extensions known to be dangerous as email attachments
DANGEROUS_EXTENSIONS = {
    ".exe",   # Windows executable
    ".bat",   # Batch script
    ".cmd",   # Windows command script
    ".js",    # JavaScript (can execute via Windows Script Host)
    ".vbs",   # VBScript
    ".ps1",   # PowerShell script
    ".zip",   # Archive (may contain malicious files inside)
    ".rar",   # Archive
    ".7z",    # Archive
    ".docm",  # Macro-enabled Word document
    ".xlsm",  # Macro-enabled Excel spreadsheet
    ".pptm",  # Macro-enabled PowerPoint presentation
    ".jar",   # Java archive (executable)
    ".scr",   # Windows screen saver (executable)
    ".hta",   # HTML application (executable)
    ".iso",   # Disk image (can autorun)
}

# Simulated fake attachment for the demo (does not need to exist on disk)
# In a real scenario this would be extracted from the email attachment.
DEMO_ATTACHMENT_FILENAME = "Invoice_March2026.pdf.exe"

# For a real file hash demonstration, we use the sample_email.eml as a
# stand-in target. The actual attachment file is simulated.
DEMO_HASH_TARGET = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "02_Evidence_Collection",
    "sample_email.eml",
)


# ── Helpers ──────────────────────────────────────────────────

def get_extension(filename):
    """Return the lowercased file extension, including the dot."""
    _, ext = os.path.splitext(filename)
    return ext.lower()


def check_double_extension(filename):
    """
    Detect double-extension tricks like 'document.pdf.exe'.
    Returns True if a double extension is detected.
    """
    parts = filename.split(".")
    # More than one extension means at least 3 dot-separated parts
    return len(parts) > 2


def calculate_hashes(filepath):
    """Calculate MD5 and SHA-256 of a file. Returns (md5, sha256) hex strings."""
    md5_h = hashlib.md5()
    sha256_h = hashlib.sha256()

    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            md5_h.update(chunk)
            sha256_h.update(chunk)

    return md5_h.hexdigest(), sha256_h.hexdigest()


def get_threat_level(extension, double_ext):
    """
    Determine the threat level based on extension and double-extension flag.

    Returns:
        str: 'HIGH', 'MEDIUM', or 'LOW'
    """
    if double_ext and extension in DANGEROUS_EXTENSIONS:
        return "CRITICAL"
    if extension in DANGEROUS_EXTENSIONS:
        return "HIGH"
    if double_ext:
        return "MEDIUM"
    return "LOW"


# ── Main ─────────────────────────────────────────────────────

def scan_attachment(attachment_filename, hash_target=None):
    """
    Perform a simulated threat assessment on an attachment.

    Args:
        attachment_filename (str): The filename of the attachment to assess.
        hash_target (str|None): Path to a real file to hash. If None, hashing
                                is skipped and a note is shown.
    """
    separator = "=" * 65
    ext = get_extension(attachment_filename)
    double_ext = check_double_extension(attachment_filename)
    threat_level = get_threat_level(ext, double_ext)

    print(separator)
    print("  ATTACHMENT THREAT SCANNER — SIMULATED ANALYSIS")
    print(separator)
    print(f"\n  Filename     : {attachment_filename}")
    print(f"  Extension    : {ext if ext else '(none)'}")

    # ── Extension check ───────────────────────────────────────
    print("\n[+] EXTENSION ANALYSIS")
    if ext in DANGEROUS_EXTENSIONS:
        print(f"  [!] Extension '{ext}' is in the DANGEROUS extensions list")
        print(f"      Reason: {_extension_description(ext)}")
    else:
        print(f"  [OK] Extension '{ext}' is not in the known-dangerous list")

    # ── Double extension check ────────────────────────────────
    print("\n[+] DOUBLE-EXTENSION CHECK")
    if double_ext:
        print(f"  [!] DOUBLE EXTENSION DETECTED in '{attachment_filename}'")
        print("      Attackers disguise executables as harmless files using")
        print("      this trick, e.g., 'invoice.pdf.exe' looks like a PDF")
        print("      but Windows may hide the final '.exe' extension.")
    else:
        print("  [OK] No double extension detected")

    # ── Hash calculation ──────────────────────────────────────
    print("\n[+] HASH CALCULATION")
    if hash_target and os.path.isfile(hash_target):
        md5, sha256 = calculate_hashes(hash_target)
        print(f"  Note: Hashing '{os.path.basename(hash_target)}' as a stand-in")
        print(f"        (real attachment not present in this simulation)")
        print(f"  MD5     : {md5}")
        print(f"  SHA-256 : {sha256}")
        print("  [i] Cross-check these hashes against VirusTotal / MalwareBazaar")
    else:
        print("  [i] No real file provided — hash calculation skipped in this demo")
        print("      In a real investigation, extract the attachment and hash it.")

    # ── Threat assessment ─────────────────────────────────────
    print("\n" + separator)
    print("[!] THREAT ASSESSMENT REPORT")
    print(separator)
    print(f"\n  Attachment   : {attachment_filename}")
    print(f"  Threat Level : {threat_level}")
    print()

    if threat_level == "CRITICAL":
        print("  VERDICT: CRITICAL THREAT — DO NOT OPEN")
        print("  This file uses a double-extension disguise AND has a")
        print("  dangerous extension. It is almost certainly malware.")
        print("  Isolate the system and escalate to incident response.")
    elif threat_level == "HIGH":
        print("  VERDICT: HIGH RISK — DO NOT OPEN")
        print("  This file type is commonly used to deliver malware.")
        print("  Submit to sandbox analysis before opening.")
    elif threat_level == "MEDIUM":
        print("  VERDICT: MEDIUM RISK — Treat with Caution")
        print("  Double extension detected. Verify with sender through")
        print("  a separate communication channel before opening.")
    else:
        print("  VERDICT: LOW RISK — No immediate indicators")
        print("  File extension appears safe, but always verify the sender.")

    print(separator)


def _extension_description(ext):
    """Return a brief description of why an extension is dangerous."""
    descriptions = {
        ".exe":  "Windows executable — can run arbitrary code",
        ".bat":  "Batch script — executes system commands",
        ".cmd":  "Command script — executes system commands",
        ".js":   "JavaScript — can execute via Windows Script Host",
        ".vbs":  "VBScript — executes system commands via Windows",
        ".ps1":  "PowerShell script — powerful scripting access",
        ".zip":  "Archive — may contain malicious files",
        ".rar":  "Archive — may contain malicious files",
        ".7z":   "Archive — may contain malicious files",
        ".docm": "Macro-enabled Word file — macros can run malware",
        ".xlsm": "Macro-enabled Excel file — macros can run malware",
        ".pptm": "Macro-enabled PowerPoint — macros can run malware",
        ".jar":  "Java archive — can execute arbitrary Java code",
        ".scr":  "Windows screen saver — treated as executable",
        ".hta":  "HTML application — executes with elevated privileges",
        ".iso":  "Disk image — can autorun or contain executables",
    }
    return descriptions.get(ext, "Known dangerous file type")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        attachment = sys.argv[1]
    else:
        attachment = DEMO_ATTACHMENT_FILENAME

    scan_attachment(attachment, hash_target=DEMO_HASH_TARGET)

# EDUCATIONAL USE ONLY
# ============================================================
# timeline_builder.py
#
# PURPOSE: Display a formatted, colour-coded incident timeline
#          for the simulated phishing attack investigation.
#
# FEATURES:
#   - Hardcoded list of timeline events (dict with timestamp,
#     description, actor, and category)
#   - Coloured output using colorama (optional — falls back to
#     plain text if colorama is not installed)
#   - Events cover the full attack lifecycle:
#       email sent → received → link clicked →
#       credentials harvested → investigation → report
#
# LIBRARY USED: Python standard library + optional colorama
# ============================================================

from datetime import datetime

# Optional: colorama for coloured terminal output
# If not installed, plain text is used instead
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


# ── Colour helpers ────────────────────────────────────────────

def red(text):
    return (Fore.RED + Style.BRIGHT + text + Style.RESET_ALL) if COLORAMA_AVAILABLE else text

def yellow(text):
    return (Fore.YELLOW + text + Style.RESET_ALL) if COLORAMA_AVAILABLE else text

def green(text):
    return (Fore.GREEN + text + Style.RESET_ALL) if COLORAMA_AVAILABLE else text

def cyan(text):
    return (Fore.CYAN + text + Style.RESET_ALL) if COLORAMA_AVAILABLE else text

def white_bold(text):
    return (Style.BRIGHT + text + Style.RESET_ALL) if COLORAMA_AVAILABLE else text


# ── Timeline events ──────────────────────────────────────────
# Each event is a dict with:
#   timestamp   : ISO 8601 string (UTC)
#   description : What happened
#   actor       : Who performed this action
#   category    : 'attack', 'victim', 'detection', 'forensic'

TIMELINE_EVENTS = [
    {
        "timestamp":   "2026-03-01T22:30:00Z",
        "description": "Attacker registers lookalike domain 'techcorp-ltd.xyz'",
        "actor":       "Attacker",
        "category":    "attack",
    },
    {
        "timestamp":   "2026-03-01T23:00:00Z",
        "description": "Attacker deploys credential-harvesting web server at 192.168.100.200",
        "actor":       "Attacker",
        "category":    "attack",
    },
    {
        "timestamp":   "2026-03-02T08:45:00Z",
        "description": "Spoofed phishing email crafted, spoofing CEO James Hartwell",
        "actor":       "Attacker",
        "category":    "attack",
    },
    {
        "timestamp":   "2026-03-02T09:14:00Z",
        "description": "Phishing email delivered to Sarah Mitchell's inbox",
        "actor":       "Mail Server",
        "category":    "attack",
    },
    {
        "timestamp":   "2026-03-02T09:22:00Z",
        "description": "Victim (Sarah Mitchell) opens the phishing email",
        "actor":       "Victim",
        "category":    "victim",
    },
    {
        "timestamp":   "2026-03-02T09:23:00Z",
        "description": "Victim clicks the malicious link in the email body",
        "actor":       "Victim",
        "category":    "victim",
    },
    {
        "timestamp":   "2026-03-02T09:23:30Z",
        "description": "Victim submits corporate credentials on fake login page",
        "actor":       "Victim",
        "category":    "victim",
    },
    {
        "timestamp":   "2026-03-02T09:23:31Z",
        "description": "Credentials harvested and stored on attacker-controlled server",
        "actor":       "Attacker",
        "category":    "attack",
    },
    {
        "timestamp":   "2026-03-02T11:45:00Z",
        "description": "IT security alert triggered; Sarah reports suspicious email",
        "actor":       "Victim / IT Security",
        "category":    "detection",
    },
    {
        "timestamp":   "2026-03-02T12:00:00Z",
        "description": "Forensic investigation initiated by Dr. Alex Patel",
        "actor":       "Investigator",
        "category":    "forensic",
    },
    {
        "timestamp":   "2026-03-02T12:30:00Z",
        "description": "Phishing email preserved as evidence; MD5 & SHA-256 hashes recorded",
        "actor":       "Investigator",
        "category":    "forensic",
    },
    {
        "timestamp":   "2026-03-02T13:00:00Z",
        "description": "Network capture (PCAP) of credential submission collected",
        "actor":       "Investigator",
        "category":    "forensic",
    },
    {
        "timestamp":   "2026-03-03T09:00:00Z",
        "description": "Full forensic analysis of email headers and URLs completed",
        "actor":       "Investigator",
        "category":    "forensic",
    },
    {
        "timestamp":   "2026-03-03T14:00:00Z",
        "description": "Indicators of Compromise (IOCs) documented; domain blocklist updated",
        "actor":       "IT Security",
        "category":    "forensic",
    },
    {
        "timestamp":   "2026-03-04T14:00:00Z",
        "description": "Full investigation report finalised and submitted to management",
        "actor":       "Investigator",
        "category":    "forensic",
    },
]

# Category labels and colours
CATEGORY_STYLES = {
    "attack":    ("ATTACK",    red),
    "victim":    ("VICTIM",    yellow),
    "detection": ("DETECTION", cyan),
    "forensic":  ("FORENSIC",  green),
}


# ── Formatting helpers ────────────────────────────────────────

def format_timestamp(iso_str):
    """Parse ISO 8601 string and return a human-readable format."""
    dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%d %b %Y  %H:%M UTC")


def print_timeline():
    """Print the full incident timeline to the console."""
    separator = "=" * 70

    print(white_bold(separator))
    print(white_bold("  INCIDENT TIMELINE — OPERATION INBOX INTRUDER"))
    print(white_bold("  Case: CASE-2026-0042 | TechCorp Ltd Phishing Attack"))
    print(white_bold(separator))

    if not COLORAMA_AVAILABLE:
        print("  [i] Install 'colorama' (pip install colorama) for coloured output\n")

    # Legend
    print("  Legend:")
    for key, (label, colour_fn) in CATEGORY_STYLES.items():
        print(f"    {colour_fn(f'[{label}]')}")
    print()

    print(white_bold(separator))

    for event in TIMELINE_EVENTS:
        label, colour_fn = CATEGORY_STYLES.get(
            event["category"], ("INFO", white_bold)
        )
        timestamp_str = format_timestamp(event["timestamp"])
        category_badge = colour_fn(f"[{label:<9}]")

        print(f"  {timestamp_str}  {category_badge}")
        print(f"  Actor : {event['actor']}")
        print(f"  Event : {event['description']}")
        print(f"  {'-' * 66}")

    print(white_bold(separator))
    print(f"  Total events: {len(TIMELINE_EVENTS)}")
    print(white_bold(separator))


if __name__ == "__main__":
    print_timeline()

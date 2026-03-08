# EDUCATIONAL USE ONLY
# ============================================================
# email_spoofing_demo.py
#
# PURPOSE  : Demonstrates how a spoofed email is CONSTRUCTED
#            using Python's standard library.
#
# IMPORTANT: This script does NOT send any email.
#            The smtplib.SMTP call is intentionally commented
#            out. The raw message is only printed to the
#            console for analysis and learning.
#
# DISCLAIMER: Understanding email spoofing is essential for
#             defenders and forensic investigators. This code
#             is provided solely to illustrate the technique
#             so that security professionals can detect and
#             prevent it. Never use this knowledge to harm
#             others or conduct unauthorised activities.
# ============================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid


def build_spoofed_email():
    """
    Constructs a simulated phishing email that spoofs the sender.

    Key concept:
      - The 'From' HEADER can display any name/address the sender chooses.
      - The actual sending address (envelope sender) is controlled by the
        SMTP server and may differ from the displayed 'From' header.
      - This mismatch is how email spoofing works and how forensic
        investigators detect it.
    """

    # --- Fictional addresses (SIMULATED ONLY) ---
    # The envelope sender — the real origin address (attacker's domain)
    envelope_sender = "ceo@techcorp-ltd.xyz"

    # The spoofed display address — appears in the victim's email client
    spoofed_from_display = "James Hartwell <j.hartwell@techcorp.co.uk>"

    # The victim's address
    recipient = "sarah.mitchell@techcorp.co.uk"

    # --- Build the MIME message ---
    msg = MIMEMultipart("alternative")

    # This is what the victim SEES in their email client — FORGED
    msg["From"] = spoofed_from_display

    # The real address — replies would go here, exposing the attacker's domain
    msg["Reply-To"] = "ceo@techcorp-ltd.xyz"

    msg["To"] = recipient
    msg["Subject"] = "URGENT: Invoice Approval Required — Action Needed Today"
    msg["Date"] = formatdate(localtime=False)

    # Message-ID reveals the true sending domain
    msg["Message-ID"] = make_msgid(domain="techcorp-ltd.xyz")

    # --- Email body ---
    body_text = (
        "Dear Sarah,\n\n"
        "I hope you are well. I am currently in an overseas meeting and "
        "unable to access the finance portal directly.\n\n"
        "Please review and approve the attached invoice (Invoice_March2026.pdf) "
        "as soon as possible — our vendor requires payment by end of day.\n\n"
        "To view the invoice, please log in using the secure link below:\n\n"
        "    http://192.168.100.200/login?ref=invoice_march2026\n\n"
        "Use your normal corporate credentials to access the document.\n\n"
        "This is time-sensitive. Please do not delay.\n\n"
        "Best regards,\n"
        "James Hartwell\n"
        "CEO, TechCorp Ltd\n"
        "Tel: +44 20 7946 0001\n"
    )

    msg.attach(MIMEText(body_text, "plain"))

    return msg, envelope_sender, recipient


def print_email_analysis(msg, envelope_sender, recipient):
    """
    Prints the raw email message and a forensic analysis of key headers.
    """
    separator = "=" * 65

    print(separator)
    print("  EMAIL SPOOFING DEMO — EDUCATIONAL SIMULATION")
    print("  No email has been sent. Output is for analysis only.")
    print(separator)

    print("\n[+] ENVELOPE INFORMATION (what the SMTP server sees)")
    print(f"    Envelope-From : {envelope_sender}")
    print(f"    Envelope-To   : {recipient}")

    print("\n[+] RAW EMAIL HEADERS (what the victim's client shows)")
    print("-" * 65)
    for key, value in msg.items():
        print(f"  {key:<15}: {value}")

    print("\n[+] RAW EMAIL MESSAGE (as it would travel across the internet)")
    print("-" * 65)
    print(msg.as_string())

    print(separator)
    print("[!] FORENSIC ANALYSIS — SPOOFING INDICATORS")
    print(separator)

    displayed_from = msg["From"]
    reply_to = msg.get("Reply-To", "Not set")
    message_id = msg.get("Message-ID", "Not set")

    print(f"\n  Displayed 'From'  : {displayed_from}")
    print(f"  Actual Envelope   : {envelope_sender}")
    print(f"  Reply-To          : {reply_to}")
    print(f"  Message-ID domain : {message_id}")

    print("\n  Spoofing indicators found:")
    print("  [!] From display domain  : techcorp.co.uk  (LEGITIMATE — spoofed)")
    print("  [!] Envelope sender      : techcorp-ltd.xyz (ATTACKER'S domain)")
    print("  [!] Reply-To domain      : techcorp-ltd.xyz (MISMATCH with From)")
    print("  [!] Message-ID domain    : techcorp-ltd.xyz (confirms origin)")
    print("  [!] URL in body          : raw IP address (192.168.100.200) — SUSPICIOUS")

    print("\n  Defensive measure: A DMARC 'reject' policy on techcorp.co.uk")
    print("  would have caused mail servers to reject this email before")
    print("  it reached the victim's inbox.")
    print(separator)

    # --- HOW SENDING WOULD WORK (intentionally not executed) ---
    # The block below shows how smtplib would be used to actually send this
    # email. It is commented out so that this script CANNOT send anything.
    #
    # with smtplib.SMTP("mail.techcorp-ltd.xyz", 25) as server:
    #     server.sendmail(
    #         from_addr=envelope_sender,   # Envelope sender (attacker's address)
    #         to_addrs=[recipient],
    #         msg=msg.as_string()
    #     )
    #
    # The From HEADER (msg["From"]) is what the recipient sees — it can be
    # set to anything.  The envelope_sender is what the SMTP server uses for
    # routing and bounce messages.  When these two differ it is a strong
    # indicator of spoofing.


if __name__ == "__main__":
    message, env_sender, to_addr = build_spoofed_email()
    print_email_analysis(message, env_sender, to_addr)

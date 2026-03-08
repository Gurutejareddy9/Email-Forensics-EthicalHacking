# Chain of Custody Document

> **EDUCATIONAL SIMULATION ONLY. All names and data are fictional.**

---

## Case Information

| Field | Value |
|---|---|
| **Case Number** | CASE-2026-0042 |
| **Case Title** | Operation Inbox Intruder — Phishing Attack on TechCorp Ltd |
| **Date Opened** | 2026-03-02 |
| **Date Closed** | 2026-03-04 |
| **Lead Investigator** | Dr. Alex Patel |
| **Organisation** | TechCorp Ltd — IT Security Team |
| **Jurisdiction** | United Kingdom |

---

## Evidence Items

| Item # | Description | File Name | File Size | MD5 Hash | SHA-256 Hash | Date Collected | Source |
|---|---|---|---|---|---|---|---|
| E-001 | Original phishing email (raw RFC 2822 format) | `sample_email.eml` | 1,448 bytes | *(calculate with hash_calculator.py)* | *(calculate with hash_calculator.py)* | 2026-03-02 12:30 UTC | Sarah Mitchell's mail client |
| E-002 | Screenshot of fake login page | `login_page_screenshot.png` | N/A | N/A | N/A | 2026-03-02 12:45 UTC | Investigator's browser |
| E-003 | Network capture (PCAP) of credential submission | `capture_20260302.pcap` | N/A | N/A | N/A | 2026-03-02 13:00 UTC | Corporate network tap |

> **Note:** For each evidence item, run `hash_calculator.py` to generate and record the actual hash values before and after every handling step.

---

## Transfer Log

| Date & Time (UTC) | Action | From | To | Hash Verified? | Notes |
|---|---|---|---|---|---|
| 2026-03-02 12:30 | Evidence collected | Sarah Mitchell (victim) | Dr. Alex Patel (investigator) | Yes — MD5 & SHA-256 recorded | Original `.eml` exported from mail client |
| 2026-03-02 12:35 | Working copy created | Dr. Alex Patel | Analysis Workstation | Yes — hashes match | Original preserved read-only on encrypted drive |
| 2026-03-02 13:00 | Evidence reviewed | Dr. Alex Patel | IT Security Manager (James Thornton) | Yes — hashes match | Briefing meeting |
| 2026-03-03 09:00 | Analysis completed | Analysis Workstation | Dr. Alex Patel | Yes — hashes match | No modifications to evidence |
| 2026-03-04 14:00 | Final report issued | Dr. Alex Patel | Management | Yes — hashes match | Investigation closed |

---

## Evidence Storage

| Location | Description | Access Restricted? |
|---|---|---|
| Encrypted USB Drive (Serial: USB-2026-001) | Original evidence — read-only copy | Yes — investigator only |
| Internal Case Management System | Working copies and analysis outputs | Yes — IT Security team only |

---

## Declaration

I certify that the evidence listed above has been collected, handled, and preserved in accordance with standard digital forensics procedures, and that the integrity of each item has been verified by cryptographic hashing at every stage.

&nbsp;

**Lead Investigator:**  Dr. Alex Patel

**Signature:** ___________________________

**Date:** 2026-03-04

&nbsp;

**Witnessed by:**  James Thornton (IT Security Manager)

**Signature:** ___________________________

**Date:** 2026-03-04

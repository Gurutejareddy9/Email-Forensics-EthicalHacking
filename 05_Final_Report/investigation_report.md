# Digital Forensics Investigation Report

---

## Cover Page

| Field | Details |
|---|---|
| **Case Title** | Operation Inbox Intruder — Phishing Attack on TechCorp Ltd |
| **Case Number** | CASE-2026-0042 |
| **Report Date** | 2026-03-04 |
| **Lead Investigator** | Dr. Alex Patel |
| **Organisation** | TechCorp Ltd — IT Security Team |
| **Classification** | Confidential (Simulated — Educational Only) |

> **⚠️ DISCLAIMER: This report is an entirely fictional, educational simulation. All names, organisations, IP addresses, domains, and events are invented. No real systems were attacked and no real data was compromised.**

---

## Table of Contents

1. [Introduction & Scope](#1-introduction--scope)
2. [Attack Simulation Summary](#2-attack-simulation-summary)
3. [Evidence Acquisition & Chain of Custody](#3-evidence-acquisition--chain-of-custody)
4. [Technical Analysis](#4-technical-analysis)
5. [Incident Timeline](#5-incident-timeline)
6. [Findings & Indicators of Compromise](#6-findings--indicators-of-compromise)
7. [Conclusions](#7-conclusions)
8. [Recommendations](#8-recommendations)
9. [References](#9-references)

---

## 1. Introduction & Scope

### 1.1 Purpose
This report documents the forensic investigation conducted in response to a phishing attack targeting TechCorp Ltd. The investigation covers the full lifecycle: attack simulation, evidence collection, technical analysis, and remediation recommendations.

### 1.2 Background
On 2026-03-02, a member of the TechCorp Ltd Finance department received a spoofed email purportedly from the CEO. The email directed the recipient to a credential-harvesting website. The victim clicked the link and submitted her corporate login credentials before the deception was discovered.

### 1.3 Scope
This investigation covers:
- The phishing email itself (headers, body, URLs)
- The attacker's infrastructure (domain, IP address)
- The victim's interaction with the malicious content
- Forensic preservation and analysis of digital evidence

The investigation does **not** cover:
- Any internal systems compromise beyond credential theft
- Third-party systems outside TechCorp Ltd's network

### 1.4 Methodology
The investigation followed the **ACPO Good Practice Guide for Digital Evidence** (UK) methodology:
1. Evidence preservation (hash and write-protect originals)
2. Examination (header, URL, and attachment analysis)
3. Analysis (correlating findings, identifying IOCs)
4. Reporting (documenting findings and recommendations)

---

## 2. Attack Simulation Summary

> This section summarises the ethical hacking phase, which modelled how the attack was carried out. All activities were simulated and no real systems were targeted.

### 2.1 Attack Type
Targeted **Spear Phishing** combined with **Email Header Spoofing**.

### 2.2 Attack Vector
The attacker:
1. Registered the lookalike domain `techcorp-ltd.xyz` (legitimate: `techcorp.co.uk`).
2. Deployed a credential-harvesting web page at `http://192.168.100.200/login`.
3. Crafted a phishing email with a forged `From` header displaying the CEO's legitimate address, while the envelope sender was `ceo@techcorp-ltd.xyz`.
4. Delivered the email to the Finance Manager's inbox.

### 2.3 Why the Attack Succeeded
- No **DMARC** policy was enforced on `techcorp.co.uk`, so the spoofed header was not rejected.
- The email used **social engineering** (urgency, authority of the CEO) to pressure the victim.
- No **MFA** was in place, so credentials alone were sufficient to access the corporate portal.

### 2.4 Tools Used (Simulated)
| Tool | Purpose |
|---|---|
| Python `smtplib` + `email` | Construct and display spoofed email headers |
| Simple HTTP server | Simulate credential-harvesting page |

---

## 3. Evidence Acquisition & Chain of Custody

### 3.1 Evidence Items

| Item # | Description | Filename | Collection Date |
|---|---|---|---|
| E-001 | Original phishing email | `sample_email.eml` | 2026-03-02 12:30 UTC |
| E-002 | Screenshot of fake login page | `login_page_screenshot.png` | 2026-03-02 12:45 UTC |
| E-003 | Network capture | `capture_20260302.pcap` | 2026-03-02 13:00 UTC |

### 3.2 Integrity Verification

All evidence items were hashed using MD5 and SHA-256 immediately upon collection. Hashes were re-verified before and after each analysis step to confirm no modification occurred. See `02_Evidence_Collection/chain_of_custody.md` for the full transfer log.

### 3.3 Storage
Original evidence was stored read-only on an encrypted USB drive accessible only to the lead investigator. Working copies were maintained on the secure internal case management system.

---

## 4. Technical Analysis

### 4.1 Email Header Analysis

The email headers were parsed using `03_Email_Analysis/header_analyzer.py`.

**Key observations:**

| Header | Value | Finding |
|---|---|---|
| `From` | `James Hartwell <j.hartwell@techcorp.co.uk>` | Display address — **forged** |
| `Reply-To` | `ceo@techcorp-ltd.xyz` | Attacker's domain — **mismatch** |
| `Message-ID` | `<20260302084500.fake001@techcorp-ltd.xyz>` | Confirms origin from attacker's domain |
| `X-Originating-IP` | `192.168.100.200` | Attacker's server IP |
| `Received` | `from mail.techcorp-ltd.xyz [192.168.100.200]` | Confirms routing through attacker's server |

**Spoofing confirmed:** The `From` display domain (`techcorp.co.uk`) does not match the `Reply-To` domain or `Message-ID` domain (`techcorp-ltd.xyz`).

### 4.2 URL Analysis

URLs were extracted from the email body using `03_Email_Analysis/url_extractor.py`.

| URL Found | Classification | Reasons |
|---|---|---|
| `http://192.168.100.200/login?ref=invoice_march2026` | **SUSPICIOUS** | Raw IP address; plain HTTP (no HTTPS); contains keyword "login" |

**Verdict:** This URL is a credential-harvesting page. The use of a raw IP address instead of a domain name, the absence of HTTPS, and the "login" keyword are all strong phishing indicators.

### 4.3 Attachment Analysis

The email referenced `Invoice_March2026.pdf.exe`. Analysed using `03_Email_Analysis/attachment_scanner.py`.

| Check | Result |
|---|---|
| Extension | `.exe` — in dangerous extensions list |
| Double extension | YES — `.pdf.exe` disguises an executable as a document |
| Threat level | **CRITICAL** |

**Verdict:** This is almost certainly malware disguised as a PDF invoice.

---

## 5. Incident Timeline

| Date & Time (UTC) | Event | Actor | Category |
|---|---|---|---|
| 2026-03-01 22:30 | Attacker registers `techcorp-ltd.xyz` | Attacker | Attack |
| 2026-03-01 23:00 | Credential-harvesting server deployed at `192.168.100.200` | Attacker | Attack |
| 2026-03-02 08:45 | Spoofed phishing email crafted | Attacker | Attack |
| 2026-03-02 09:14 | Email delivered to victim's inbox | Mail Server | Attack |
| 2026-03-02 09:22 | Victim opens the phishing email | Victim | Victim action |
| 2026-03-02 09:23 | Victim clicks malicious link | Victim | Victim action |
| 2026-03-02 09:23:30 | Victim submits credentials on fake page | Victim | Victim action |
| 2026-03-02 09:23:31 | Credentials harvested by attacker | Attacker | Attack |
| 2026-03-02 11:45 | Security alert triggered; victim reports email | IT Security | Detection |
| 2026-03-02 12:00 | Forensic investigation begins | Investigator | Forensic |
| 2026-03-02 12:30 | Evidence collected and hashed | Investigator | Forensic |
| 2026-03-03 09:00 | Full technical analysis completed | Investigator | Forensic |
| 2026-03-04 14:00 | Investigation report finalised | Investigator | Forensic |

> Full colour-coded timeline: run `python 04_Timeline_and_Findings/timeline_builder.py`

---

## 6. Findings & Indicators of Compromise

### 6.1 Key Findings

1. The phishing email successfully bypassed the email gateway due to the absence of DMARC enforcement.
2. Email header spoofing was confirmed: the `From` display domain differed from the true sending domain.
3. A lookalike domain (`techcorp-ltd.xyz`) was used to host both the mail server and the credential-harvesting page.
4. The malicious URL used a raw IP address and plain HTTP — clear indicators of a phishing page.
5. The referenced attachment used a double-extension trick to disguise an executable.
6. Corporate credentials of one user were confirmed compromised.

### 6.2 Indicators of Compromise (IOCs)

> All IOCs below are **fictional / simulated**.

| Type | Value | Role |
|---|---|---|
| IP Address | `192.168.100.200` | Attacker's server |
| Domain | `techcorp-ltd.xyz` | Lookalike / attacker domain |
| Email | `ceo@techcorp-ltd.xyz` | Attacker's sending address |
| URL | `http://192.168.100.200/login?ref=invoice_march2026` | Credential-harvesting page |
| File | `Invoice_March2026.pdf.exe` | Malware (simulated) |

---

## 7. Conclusions

This investigation confirms that TechCorp Ltd was targeted by a sophisticated spear phishing attack in which the attacker:

- Registered a lookalike domain to impersonate the corporate mail infrastructure.
- Spoofed the CEO's email address to exploit authority and urgency.
- Hosted a credential-harvesting page that successfully captured one employee's login details.

The attack succeeded primarily because of the absence of email authentication standards (SPF, DKIM, DMARC) and multi-factor authentication. The victim's credentials were compromised within 9 minutes of the email being delivered — highlighting how effective social engineering can be.

The digital forensics investigation was able to definitively attribute the attack to the `techcorp-ltd.xyz` infrastructure using email header analysis, URL analysis, and the chain of custody records.

---

## 8. Recommendations

### Immediate
1. Reset the compromised user's credentials and revoke all active sessions.
2. Block `techcorp-ltd.xyz` and `192.168.100.200` at the email gateway and firewall.
3. Enable MFA for all corporate portal logins.

### Short-Term (within 30 days)
4. Publish an **SPF record** for `techcorp.co.uk`.
5. Configure **DKIM signing** on all outbound email.
6. Publish a **DMARC record** with `p=reject`.
7. Configure email gateway to flag `From`/`Reply-To` domain mismatches.

### Long-Term
8. Conduct regular **phishing simulation exercises** for all staff.
9. Deliver **security awareness training** covering social engineering tactics.
10. Commission annual **email security penetration tests**.
11. Implement **SIEM alerting** for anomalous login activity (new location, new device).

---

## 9. References

| Tool / Resource | Purpose in Investigation |
|---|---|
| **Python 3** (`email`, `hashlib`, `re`, `datetime`) | Email parsing, hash calculation, URL extraction, timeline building |
| **Autopsy** | Open-source digital forensics platform for disk and file analysis |
| **Wireshark** | Network packet capture and analysis (referenced for PCAP evidence) |
| **VirusTotal** | Online threat intelligence for hash and URL lookups |
| **MXToolbox** | Email header analysis and SPF/DKIM/DMARC record checks |
| **ACPO Good Practice Guide for Digital Evidence** | Forensic methodology framework |
| **RFC 2822** | Internet Message Format standard (email structure) |
| **RFC 7489** | DMARC specification |

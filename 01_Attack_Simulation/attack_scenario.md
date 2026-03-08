# Attack Scenario — Simulated Cybercrime Narrative

> **EDUCATIONAL SIMULATION ONLY. All names, companies, IP addresses, and events are entirely fictional.**

---

## Case Title
**Operation Inbox Intruder — Phishing Attack on TechCorp Ltd**

## Case Number
`CASE-2026-0042`

## Scenario Overview

A targeted phishing and email-spoofing attack was launched against **TechCorp Ltd**, a mid-sized software development company based in London, UK. The attacker impersonated the company's CEO to trick an employee in the Finance department into clicking a malicious link and submitting their corporate credentials.

---

## Actors

| Role | Name (Fictional) | Details |
|---|---|---|
| **Victim** | Sarah Mitchell | Finance Manager, TechCorp Ltd |
| **Attacker** | Unknown (alias: `phantom_mailer`) | External threat actor |
| **CEO (Spoofed)** | James Hartwell | CEO, TechCorp Ltd (did NOT send the email) |
| **Forensic Investigator** | Dr. Alex Patel | Internal IT Security team |

---

## Attack Description

The attacker registered a lookalike domain `techcorp-ltd.xyz` (the legitimate domain is `techcorp.co.uk`) and configured it with a basic mail server. Using Python's `smtplib`, the attacker crafted a spoofed email that displayed James Hartwell's legitimate address (`j.hartwell@techcorp.co.uk`) in the **From** header, while the actual sending address was `ceo@techcorp-ltd.xyz`.

The email contained:
1. An **urgent message** claiming that an invoice needed immediate approval.
2. A **fake link** pointing to `http://192.168.100.200/login` — a credential-harvesting page hosted on an attacker-controlled server.
3. A reference to a **fake invoice attachment** (`Invoice_March2026.pdf.exe`) to lend credibility.

The victim, Sarah Mitchell, received the email at 09:14 on **2026-03-02**, believed it was from her CEO, and clicked the link. She entered her corporate username and password on the fake login page. The credentials were silently recorded by the attacker's server.

---

## Attack Timeline

| Date & Time (UTC) | Event | Actor |
|---|---|---|
| 2026-03-01 22:30 | Attacker registers lookalike domain `techcorp-ltd.xyz` | Attacker |
| 2026-03-01 23:00 | Attacker sets up credential-harvesting web server at `192.168.100.200` | Attacker |
| 2026-03-02 08:45 | Spoofed phishing email crafted and queued for delivery | Attacker |
| 2026-03-02 09:14 | Phishing email delivered to Sarah Mitchell's inbox | Mail Server |
| 2026-03-02 09:22 | Sarah opens the email and clicks the malicious link | Victim |
| 2026-03-02 09:23 | Victim submits credentials on fake login page | Victim |
| 2026-03-02 09:23 | Credentials harvested and stored by attacker server | Attacker |
| 2026-03-02 11:45 | IT security alerts triggered; Sarah reports suspicious email | Victim / IT |
| 2026-03-02 12:00 | Forensic investigation initiated by Dr. Alex Patel | Investigator |
| 2026-03-02 12:30 | Original phishing email preserved as evidence (`.eml` file hashed) | Investigator |
| 2026-03-03 09:00 | Full forensic analysis of email headers and URLs completed | Investigator |
| 2026-03-04 14:00 | Investigation report finalised | Investigator |

---

## Impact

- Corporate credentials of one Finance Manager compromised.
- Potential exposure of sensitive financial data.
- Reputational risk to TechCorp Ltd.

---

## Lessons Learned

1. **SPF, DKIM, and DMARC** were not enforced on the company's mail gateway — allowing spoofed emails to pass through.
2. Users lacked **phishing awareness training**.
3. No **multi-factor authentication (MFA)** was in place for the corporate portal.

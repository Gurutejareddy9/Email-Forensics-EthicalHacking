# Findings Report

> **Case:** CASE-2026-0042 — Operation Inbox Intruder
> **Date:** 2026-03-04
> **Investigator:** Dr. Alex Patel

---

## Executive Summary

On 2026-03-02, a targeted phishing email was delivered to Sarah Mitchell, Finance Manager at TechCorp Ltd. The email spoofed the identity of the company CEO (James Hartwell) and directed the victim to a credential-harvesting website hosted at IP address `192.168.100.200`. The victim's corporate credentials were compromised. Forensic analysis confirmed the email originated from a lookalike domain (`techcorp-ltd.xyz`) controlled by the attacker and identified multiple technical indicators of spoofing.

---

## Key Findings

- **Spoofed From Header:** The email displayed `j.hartwell@techcorp.co.uk` as the sender, but the actual envelope sender was `ceo@techcorp-ltd.xyz`.
- **Lookalike Domain:** The attacker registered `techcorp-ltd.xyz` — visually similar to the legitimate `techcorp.co.uk` — to host their mail server and credential-harvesting page.
- **Reply-To Mismatch:** The `Reply-To` header pointed to `ceo@techcorp-ltd.xyz`, exposing the attacker's domain when the victim replied.
- **Malicious URL:** The email body contained a hyperlink to `http://192.168.100.200/login?ref=invoice_march2026` — a plain-HTTP credential-harvesting page on the attacker's server.
- **Suspicious IP:** The `X-Originating-IP` header revealed `192.168.100.200`, consistent with the attacker-controlled server.
- **Double-Extension Attachment Reference:** A filename `Invoice_March2026.pdf.exe` was referenced — a classic technique to disguise an executable as a document.
- **No DMARC Enforcement:** TechCorp Ltd did not have a DMARC `reject` policy, allowing the spoofed email to pass through mail gateway checks.
- **No MFA:** The absence of multi-factor authentication meant stolen credentials could be immediately exploited.

---

## Indicators of Compromise (IOCs)

> ⚠️ All IOCs below are **fictional / simulated** and do not represent real threats.

### IP Addresses

| IP Address | Role |
|---|---|
| `192.168.100.200` | Attacker's mail server and credential-harvesting web server |

### Domains

| Domain | Role |
|---|---|
| `techcorp-ltd.xyz` | Lookalike domain registered by attacker |
| `mail.techcorp-ltd.xyz` | Attacker's SMTP mail server |

### Email Addresses

| Address | Role |
|---|---|
| `ceo@techcorp-ltd.xyz` | Attacker's sending address (envelope sender) |
| `j.hartwell@techcorp.co.uk` | Legitimate CEO address that was **spoofed** (victim of impersonation) |

### URLs

| URL | Classification |
|---|---|
| `http://192.168.100.200/login?ref=invoice_march2026` | Credential-harvesting page |

### File Hashes (simulated attachment)

| Filename | MD5 | SHA-256 |
|---|---|---|
| `Invoice_March2026.pdf.exe` | *(simulated — not a real file)* | *(simulated — not a real file)* |

---

## Recommendations

### Immediate Actions
1. **Reset compromised credentials** — Change Sarah Mitchell's corporate password and revoke any active sessions immediately.
2. **Block the attacker's domain and IP** — Add `techcorp-ltd.xyz` and `192.168.100.200` to the email gateway and firewall blocklists.
3. **Enable MFA** — Implement multi-factor authentication for all corporate portal logins to prevent stolen credentials being used.

### Short-Term Actions
4. **Implement SPF** — Publish an SPF record for `techcorp.co.uk` to authorise only legitimate mail servers.
5. **Implement DKIM** — Configure DKIM signing on all outbound email from `techcorp.co.uk`.
6. **Enforce DMARC** — Publish a DMARC record with `p=reject` to instruct receiving mail servers to reject emails that fail SPF/DKIM.
7. **Email gateway rules** — Configure rules to flag emails where the `From` display domain differs from the `Reply-To` domain.

### Long-Term Actions
8. **Phishing awareness training** — Conduct regular simulated phishing exercises and train employees to:
   - Hover over links before clicking to verify the destination URL.
   - Call the sender through a known number to verify urgent financial requests.
   - Report suspicious emails to the IT security team.
9. **Incident response plan** — Document and rehearse the company's incident response procedure to reduce investigation time in future incidents.
10. **Regular penetration testing** — Commission annual email security assessments to identify weaknesses before attackers do.

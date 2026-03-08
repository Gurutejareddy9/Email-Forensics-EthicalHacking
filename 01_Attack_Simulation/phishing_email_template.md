# Phishing Email Template — Annotated Example

> **EDUCATIONAL SIMULATION ONLY. This email is entirely fictional and was never sent.**

---

## Raw Email (Simulated)

```
From: James Hartwell <j.hartwell@techcorp.co.uk>
To: sarah.mitchell@techcorp.co.uk
Subject: URGENT: Invoice Approval Required — Action Needed Today
Date: Mon, 02 Mar 2026 08:45:00 +0000
Reply-To: ceo@techcorp-ltd.xyz
Message-ID: <20260302084500.fake001@techcorp-ltd.xyz>

Dear Sarah,

I hope you are well. I am currently in an overseas meeting and unable to 
access the finance portal directly.

Please review and approve the attached invoice (Invoice_March2026.pdf) 
as soon as possible — our vendor requires payment by end of day.

To view the invoice, please log in using the secure link below:

    http://192.168.100.200/login?ref=invoice_march2026

Use your normal corporate credentials to access the document.

This is time-sensitive. Please do not delay.

Best regards,
James Hartwell
CEO, TechCorp Ltd
Tel: +44 20 7946 0001
```

---

## Annotation — Why Each Part is Suspicious

| Email Field / Element | What It Shows | Why It Is Suspicious |
|---|---|---|
| **From:** `j.hartwell@techcorp.co.uk` | Appears to be the CEO's real address | This header can be **forged** — the envelope sender is different. Always check the mail server logs. |
| **Reply-To:** `ceo@techcorp-ltd.xyz` | Replies would go to a *different* domain | The domain `techcorp-ltd.xyz` is a **lookalike domain** registered by the attacker, not the company's real domain `techcorp.co.uk`. |
| **Message-ID:** `...@techcorp-ltd.xyz` | Message originated from `techcorp-ltd.xyz` | Confirms the email was sent from the **attacker's domain**, not the corporate mail server. |
| **Subject:** "URGENT … Action Needed Today" | Creates time pressure | Classic **social engineering** tactic — urgency prevents the victim from thinking critically. |
| **Body: Overseas meeting, can't access portal** | Explains why CEO can't act himself | Creates a believable excuse while bypassing normal verification channels. |
| **Link:** `http://192.168.100.200/login` | Points to a raw IP address | Legitimate corporate portals **never** use raw IP addresses. This is a credential-harvesting page. The URL also lacks HTTPS. |
| **Link query param:** `?ref=invoice_march2026` | Adds fake context to the URL | Makes the link look purposeful; used to track which victim clicked. |
| **Attachment reference:** `Invoice_March2026.pdf` | Implies a real document | No attachment is actually present in this email; the link substitutes for it. Real phishing emails may attach malware disguised as a PDF. |
| **Sender tone:** "Please do not delay" | Pressures victim to act without verifying | Discourages the victim from calling the CEO or checking with colleagues. |

---

## Phishing Indicators Summary

- ✅ **Spoofed From header** (display address ≠ envelope sender)
- ✅ **Lookalike domain** in Reply-To and Message-ID
- ✅ **Urgency and authority** social engineering
- ✅ **Suspicious URL** using raw IP address, no HTTPS
- ✅ **Request for credentials** via an external link
- ✅ **Impersonation** of a high-authority figure (CEO)

---

## Defensive Measures That Would Have Caught This

1. **DMARC policy** (`reject`) on `techcorp.co.uk` — would have blocked spoofed From headers.
2. **Email gateway** flagging `Reply-To` domain mismatch.
3. **User training** to hover over links and verify the domain before clicking.
4. **MFA** — even if credentials were stolen, the attacker could not log in without the second factor.

# 📧 Email Forensics & Ethical Hacking

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Educational](https://img.shields.io/badge/Purpose-Educational-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> **⚠️ DISCLAIMER: This project is strictly for educational and academic purposes only. All data, IP addresses, domains, email addresses, and scenarios are entirely fictional and simulated. No real attacks are performed.**

---

## 📖 Project Description

This repository combines two related academic projects into one comprehensive, presentation-ready resource:

### 1. End-to-End Digital Forensics Investigation of an Email-Based Cybercrime
A structured digital forensics investigation workflow covering evidence acquisition, chain of custody, email header analysis, URL extraction, and a full investigation report — following real-world forensic methodologies.

### 2. Secure Email Communication: Attack Simulation & Forensics
An ethical hacking simulation demonstrating how phishing and email spoofing attacks are constructed, how forensic investigators detect them, and what defensive measures organisations can implement.

---

## 🗂️ Repository Structure

```
Email-Forensics-EthicalHacking/
│
├── README.md                              ← This file
├── requirements.txt                       ← Python dependencies
│
├── 01_Attack_Simulation/
│   ├── attack_scenario.md                 ← Narrative of the simulated cybercrime
│   ├── phishing_email_template.md         ← Annotated phishing email example
│   └── email_spoofing_demo.py             ← Python script: builds spoofed email (no send)
│
├── 02_Evidence_Collection/
│   ├── sample_email.eml                   ← Realistic fake phishing email (RFC 2822)
│   ├── hash_calculator.py                 ← MD5 & SHA-256 hash calculator for evidence
│   └── chain_of_custody.md               ← Chain of custody document template
│
├── 03_Email_Analysis/
│   ├── header_analyzer.py                 ← Parses & flags suspicious email headers
│   ├── url_extractor.py                   ← Extracts & flags URLs from email body
│   └── attachment_scanner.py             ← Simulates attachment threat assessment
│
├── 04_Timeline_and_Findings/
│   ├── timeline_builder.py               ← Prints colour-coded incident timeline
│   └── findings_report.md               ← Key findings, IOCs & recommendations
│
└── 05_Final_Report/
    └── investigation_report.md           ← Full professional forensic report
```

---

## 🚀 How to Run the Scripts

### Prerequisites
```bash
python --version   # Python 3.8 or higher required
pip install colorama   # Optional — for coloured terminal output
```

### Run Each Script
```bash
# 1. Build a simulated spoofed email (no email is sent)
python 01_Attack_Simulation/email_spoofing_demo.py

# 2. Calculate hashes of the sample evidence file
python 02_Evidence_Collection/hash_calculator.py

# 3. Analyse email headers for spoofing indicators
python 03_Email_Analysis/header_analyzer.py

# 4. Extract and flag URLs from the email body
python 03_Email_Analysis/url_extractor.py

# 5. Simulate an attachment threat scan
python 03_Email_Analysis/attachment_scanner.py

# 6. Print the incident timeline
python 04_Timeline_and_Findings/timeline_builder.py
```

All scripts use only **Python standard library** (plus optional `colorama`). No other external packages are required.

---

## 🛠️ Tools & Technologies

| Tool / Library | Purpose |
|---|---|
| Python 3 (stdlib) | All analysis scripts |
| `email` | Parsing RFC 2822 email files |
| `hashlib` | MD5 & SHA-256 integrity hashing |
| `re` | Regular expression URL extraction |
| `datetime` | Timestamp handling in timeline |
| `colorama` *(optional)* | Coloured terminal output |
| Autopsy *(reference)* | Disk & file forensics (mentioned in report) |
| Wireshark *(reference)* | Network packet analysis (mentioned in report) |
| VirusTotal *(reference)* | Online threat intelligence (mentioned in report) |

---

## 📚 Project Phases

| Phase | Folder | Description |
|---|---|---|
| 1 | `01_Attack_Simulation` | Ethical hacking: simulate the phishing attack |
| 2 | `02_Evidence_Collection` | Acquire & preserve digital evidence |
| 3 | `03_Email_Analysis` | Technical forensic analysis |
| 4 | `04_Timeline_and_Findings` | Build incident timeline & document findings |
| 5 | `05_Final_Report` | Full professional investigation report |

---

## ⚖️ Disclaimer

All content in this repository is **fictional and created solely for educational purposes**. This project does **not** promote, facilitate, or condone any malicious activity. The techniques described are presented to help students understand cybersecurity threats and how to defend against them.

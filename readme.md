# 🐾 ShellClaw – PowerShell Defense Engine

## Overview
**ShellClaw** is a lightweight, SYSTEM-level PowerShell hardening and bypass detection tool.  
It monitors PowerShell executions in real-time, detects suspicious behaviors like `-ExecutionPolicy Bypass`, `-nop`, and `-EncodedCommand`, and logs all findings for forensics.

---

## Key Features
- SYSTEM-context WMI-based detection (persistent across reboots).
- Dynamic logging with fallback (`C:\Users\Public\ShellClawDetection.log` or `C:\Windows\Temp`).
- Real-time defense with minimal dependencies.
- Standalone executable (packaged with PyInstaller).

---

## Getting Started
1. **Download & extract** `ShellClaw_v1.0.0.zip`.
2. **Verify SHA256 checksum**:
   ```powershell
   certutil -hashfile ShellClaw_v1.0.0.zip SHA256

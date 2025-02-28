# ShellClaw: Endpoint Defense

ShellClaw is a lightweight endpoint security tool designed to harden Windows systems by implementing security best practices, particularly focused on PowerShell hardening and threat detection. Developed by DataCats, it provides essential security capabilities for environments without advanced AV or EDR solutions.

## Features

- **PowerShell Hardening**: Configure execution policies, enable script logging, and disable legacy PowerShell v2
- **Enhanced Logging**: Implement comprehensive logging for suspicious activity detection
- **WMI Detection**: Monitor for suspicious WMI activities commonly used in attacks
- **Process Monitoring**: View and analyze running processes for suspicious activity
- **Master Control Panel**: Easily manage and monitor all security features
- **Customizable Settings**: Tailor security controls to your environment
- **Dark Mode Support**: Easy on the eyes during those late-night security sessions

## Prerequisites

- Windows 10/11 or Windows Server 2016+
- Python 3.8 or higher
- PyQt5

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/datacats-v3xx/ShellClaw.git
   ```

2. Set up a Python environment (optional but recommended):
   ```
   conda create -n DataCats-ShellClaw python=3.9
   conda activate DataCats-ShellClaw
   ```
   
   Or using venv:
   ```
   python -m venv shellclaw-env
   shellclaw-env\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install PyQt5
   ```

## Usage

### Running ShellClaw

For full functionality, run as administrator:
- Right-click on Command Prompt/PowerShell and select "Run as administrator"
- Navigate to your project directory
- Run `python shellclaw.py`

### Hardening Controls

The Hardening Controls tab provides options to:
- Set PowerShell execution policy to AllSigned (requires admin)
- Enable comprehensive PowerShell logging (requires admin)
- Disable PowerShell v2 to eliminate legacy attack vectors (requires admin)
- Configure WMI activity monitoring

### Detection Logs

The Detection Logs tab displays security events and alerts, including:
- PowerShell script execution
- Suspicious command patterns
- WMI activities
- Authentication attempts

## Project Structure

```
shellclaw/
├── shellclaw.py         # Main entry point
├── ui/                  # UI components 
│   ├── __init__.py
│   ├── shellclaw_ui.py  # Main UI class
│   └── settings_tab.py  # Settings tab implementation
├── core/                # Core functionality
│   ├── __init__.py
│   ├── forensics.py     # Forensics and detection functionality
│   ├── hardening.py     # System hardening functions
│   └── settings.py      # Settings management
└── utils/               # Utility functions
    ├── __init__.py
    └── admin.py         # Administrator privilege management
```

## Security Benefits

ShellClaw implements several security measures recommended by experts:

1. **PowerShell Hardening**
   - Restricts execution policy to signed scripts only
   - Enables comprehensive logging of PowerShell activities
   - Disables legacy PowerShell v2 (often used to bypass monitoring)

2. **Enhanced Detection**
   - Monitors for suspicious command patterns
   - Tracks WMI usage (commonly leveraged in attacks)
   - Logs security-relevant events for investigation

3. **Preventative Controls**
   - Implements security best practices proactively
   - Reduces attack surface through configuration hardening

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the tool.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Developed by DataCats for endpoint security enhancement
- Inspired by PowerShell security best practices and MITRE ATT&CK techniques

---

*ShellClaw is provided as-is without warranty. Always test security tools in a controlled environment before deploying to production systems.*

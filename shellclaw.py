# shellclaw.py
from ui.shellclaw_ui import ShellClawUI
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShellClawUI()
    window.show()
    sys.exit(app.exec_())
import ctypes
if not ctypes.windll.shell32.IsUserAnAdmin():
    raise PermissionError("❌ ShellClaw requires Administrator privileges. Please run PyCharm as Administrator.")
from core.detection import create_wmi_detection
import core.hardening
print(dir(core.hardening))
from core.hardening import set_execution_policy, enable_logging, disable_ps_v2
from core.detection import create_wmi_detection
from core.forensics import log_detection

def main():
    print("🐾 ShellClaw: PowerShell Defense Engine Initializing...")

    # 1. Apply essential hardening (personal mode default for now)
    print("🔒 Setting Execution Policy to AllSigned...")
    result = set_execution_policy("AllSigned")
    log_detection(result["output"] if result["success"] else result["error"])

    print("📝 Enabling PowerShell Logging...")
    for res in enable_logging():
        log_detection(res["output"] if res["success"] else res["error"])

    print("🛡️ Disabling PowerShell v2...")
    v2_result = disable_ps_v2()
    log_detection(v2_result["output"] if v2_result["success"] else v2_result["error"])

    # 2. Activate real-time bypass detection
    print("⚡ Activating Real-Time Detection (ShellClaw WMI Watch)...")
    create_wmi_detection()

    print("✅ ShellClaw is watching. Stay sharp. 🐾")

if __name__ == "__main__":
    main()

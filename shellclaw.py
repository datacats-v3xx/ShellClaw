# shellclaw.py
from PyQt5.QtWidgets import QApplication
from ui.shellclaw_ui import ShellClawUI
import sys


def main():
    print("🐾 ShellClaw: Consumer Endpoint Defense Initializing...")

    app = QApplication(sys.argv)
    window = ShellClawUI()
    window.show()
    print(" Entering main event loop...")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

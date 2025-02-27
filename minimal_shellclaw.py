# shellclaw_fixed.py - Restructured initialization sequence
import sys
import os
import logging

# Setup logging first
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/shellclaw_debug.log',
    filemode='w'
)


def main():
    print("🐾 ShellClaw: Consumer Endpoint Defense Initializing...")

    # Import UI framework first (before any core modules)
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    # Initialize core modules (in a controlled sequence)
    print("Initializing core modules...")
    # Use lazy imports to control initialization sequence
    from core.forensics import log_detection
    log_detection("ShellClaw starting up")

    # Initialize utils first (needed by other modules)
    import core.utils

    # Import but don't initialize master_hardening yet
    import core.master_hardening
    # Now initialize it
    if hasattr(core.master_hardening, "initialize"):
        core.master_hardening.initialize()

    # Create UI last, after all modules are initialized
    print("Initializing UI...")
    from ui.shellclaw_ui import ShellClawUI
    window = ShellClawUI()
    window.show()

    print("Entering main event loop...")
    return app.exec_()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}")
        import traceback

        logging.error(traceback.format_exc())
        print(f"ERROR: {str(e)}")
        print("Check logs/shellclaw_debug.log for details")
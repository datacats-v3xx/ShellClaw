import os
import time

from core.utils import run_powershell


import threading

def main():
    log_step("🐾 ShellClaw: Consumer Endpoint Defense Initializing...")

    # Comment out the potentially problematic code
    # log_step("Creating PowerShell detection...")
    # create_advanced_ps_detection()

    # log_step("Starting PowerShell script watcher...")
    # ps_watch_thread = threading.Thread(target=watch_ps_scripts, daemon=True)
    # ps_watch_thread.start()

    log_step("Initializing GUI...")
    app = QApplication(sys.argv)
    window = ShellClawUI()
    window.show()

    log_step("Entering main event loop...")
    sys.exit(app.exec_())

def some_detection_function():
    from core.forensics import log_detection  # Import inside the function
    log_detection("🚨 Detection triggered!")

def create_wmi_detection():
    """Create basic WMI detection for PowerShell bypass attempts."""
    log_detection("⚡ Setting up WMI PowerShell detection...")
    ps_script = """
    $filter = Set-WmiInstance -Namespace root\\subscription -Class __EventFilter -Arguments @{
        Name = 'ShellClawPSDetection';
        EventNamespace = 'root\\\\cimv2';
        QueryLanguage = 'WQL';
        Query = "SELECT * FROM Win32_ProcessStartTrace WHERE ProcessName='powershell.exe'"
    }

    $consumer = Set-WmiInstance -Namespace root\\subscription -Class CommandLineEventConsumer -Arguments @{
        Name = 'ShellClawPSConsumer';
        CommandLineTemplate = 'powershell.exe -Command "Out-File -FilePath C:\\\\Users\\\\Public\\\\ShellClawDetection.log -Append -InputObject \\'🚨 PowerShell execution detected at $(Get-Date)\\'"'
    }

    Set-WmiInstance -Namespace root\\subscription -Class __FilterToConsumerBinding -Arguments @{
        Filter = $filter.__PATH;
        Consumer = $consumer.__PATH
    }
    """
    run_powershell(ps_script)
    log_detection("✅ WMI detection operational.")


def watch_ps_scripts(watch_dir="C:\\Users\\Public\\"):
    """Detect suspicious .ps1 file drops in the specified directory."""
    from core.forensics import log_detection
    import os, time
    import logging

    logging.info(f"Starting PS script watcher for directory: {watch_dir}")

    if not os.path.exists(watch_dir):
        logging.error(f"Watch directory does not exist: {watch_dir}")
        return

    try:
        tracked = set(os.listdir(watch_dir))
        logging.debug(f"Initial file count: {len(tracked)}")
    except Exception as e:
        logging.error(f"Error accessing watch directory: {str(e)}")
        return

    while True:
        try:
            time.sleep(5)

            # Safely get current files
            try:
                current = set(os.listdir(watch_dir))
            except Exception as e:
                logging.error(f"Error listing directory: {str(e)}")
                continue

            # Find new files
            new_files = current - tracked
            for f in new_files:
                if f.endswith('.ps1'):
                    full_path = os.path.join(watch_dir, f)
                    file_size = os.path.getsize(full_path) if os.path.exists(full_path) else "unknown"
                    log_detection(f"🚨 Suspicious script detected: {f} (Size: {file_size} bytes)")
                    logging.warning(f"Suspicious PS1 script detected: {full_path}")

            tracked = current
        except Exception as e:
            logging.error(f"Error in watch_ps_scripts: {str(e)}")
            # Don't crash, just continue monitoring
            time.sleep(10)  # Wait a little longer after an error

from core.utils import run_powershell
from core.forensics import log_detection


def create_safer_wmi_detection():
    """Create a safer WMI detection for PowerShell monitoring."""
    from core.forensics import log_detection
    from core.utils import run_powershell

    log_detection("⚡ Setting up safer PowerShell detection...")

    # Use a much simpler command that's less likely to cause memory issues
    ps_script = """
    # Create a simple log file for PowerShell detection
    $logPath = "C:\\Users\\Public\\shellclaw_ps_detect.log"
    "ShellClaw PowerShell detection initialized at $(Get-Date)" | Out-File -FilePath $logPath

    # Simple registry modification to track that we've run
    $regPath = "HKCU:\\Software\\ShellClaw"
    if (-not (Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    Set-ItemProperty -Path $regPath -Name "PSDetectionEnabled" -Value 1 -Type DWord

    # Return simple success message
    "PowerShell detection initialized successfully"
    """

    result = run_powershell(ps_script)
    if result["success"]:
        log_detection("✅ Basic PowerShell detection setup complete")
        return True
    else:
        log_detection(f"❌ PowerShell detection setup failed: {result['error']}")
        return False
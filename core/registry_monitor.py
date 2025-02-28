import time
import threading
from core.utils import run_powershell
from core.forensics import log_detection


def start_registry_monitoring():
    """Start monitoring registry for changes to sensitive keys."""
    thread = threading.Thread(target=_registry_monitor_thread, daemon=True)
    thread.start()
    return thread


def _registry_monitor_thread():
    """Background thread that monitors registry changes."""
    log_detection(" Registry monitoring started")

    # PowerShell script to create WMI event for registry changes
    ps_script = """
    $filter = Set-WmiInstance -Namespace root\\subscription -Class __EventFilter -Arguments @{
        Name = 'ShellClawRegistryMonitor';
        EventNamespace = 'root\\default';
        QueryLanguage = 'WQL';
        Query = "SELECT * FROM RegistryTreeChangeEvent WHERE 
                Hive='HKEY_LOCAL_MACHINE' AND 
                (KeyPath='SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run' OR 
                 KeyPath LIKE 'SOFTWARE\\\\Microsoft\\\\Windows NT\\\\CurrentVersion\\\\Winlogon%' OR
                 KeyPath LIKE 'SYSTEM\\\\CurrentControlSet\\\\Services%')"
    }

    $consumer = Set-WmiInstance -Namespace root\\subscription -Class CommandLineEventConsumer -Arguments @{
        Name = 'ShellClawRegistryConsumer';
        CommandLineTemplate = 'powershell.exe -Command "Out-File -FilePath C:\\\\Users\\\\Public\\\\ShellClawRegistry.log -Append -InputObject \\'🔑 Registry change detected: $($TargetInstance.Hive)\\\\$($TargetInstance.KeyPath) at $(Get-Date)\\'"'
    }

    Set-WmiInstance -Namespace root\\subscription -Class __FilterToConsumerBinding -Arguments @{
        Filter = $filter.__PATH;
        Consumer = $consumer.__PATH
    }
    """

    result = run_powershell(ps_script)
    if result["success"]:
        log_detection("✅ Registry monitoring WMI event created")
    else:
        log_detection(f"❌ Failed to create registry monitor: {result['error']}")

    # Continue monitoring the log file
    registry_log = "C:\\Users\\Public\\ShellClawRegistry.log"
    last_size = 0

    while True:
        try:
            import os
            if os.path.exists(registry_log):
                current_size = os.path.getsize(registry_log)
                if current_size > last_size:
                    with open(registry_log, "r") as f:
                        f.seek(last_size)
                        new_entries = f.read()
                        for line in new_entries.splitlines():
                            log_detection(line)
                    last_size = current_size
        except Exception as e:
            log_detection(f" Registry monitor error: {str(e)}")

        time.sleep(10)  # Check every 10 seconds
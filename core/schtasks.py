# Scheduled task to run WMI as SYSTEM since running perm isn't ideal. Working theory.
import subprocess
from core.forensics import log_detection

def create_wmi_detection():
    """Setup WMI subscriptions via SYSTEM context using Scheduled Tasks."""
    log_detection("⚡ Attempting WMI subscription setup via SYSTEM context...")

    # PowerShell script for WMI creation
    ps_script = """
    $filter = Set-WmiInstance -Namespace root\\subscription -Class __EventFilter -Arguments @{
        Name = 'ShellClawBypassDetection';
        EventNamespace = 'root\\cimv2';
        QueryLanguage = 'WQL';
        Query = "SELECT * FROM Win32_ProcessStartTrace WHERE ProcessName='powershell.exe' AND CommandLine LIKE '%-ep Bypass%'"
    }
    $consumer = Set-WmiInstance -Namespace root\\subscription -Class CommandLineEventConsumer -Arguments @{
        Name = 'ShellClawBypassAlert';
        CommandLineTemplate = 'powershell.exe -Command \\"Out-File -FilePath C:\\\\ShellClawDetection.log -Append -InputObject \\'🚨 Detected bypass attempt!\\'\\"'
    }
    Set-WmiInstance -Namespace root\\subscription -Class __FilterToConsumerBinding -Arguments @{
        Filter = $filter.__PATH;
        Consumer = $consumer.__PATH
    }
    """

    # Create a temporary PowerShell script
    with open("C:\\ShellClawWMISetup.ps1", "w", encoding="utf-8") as script_file:
        script_file.write(ps_script)

    # Create a scheduled task that runs as SYSTEM
    subprocess.run([
        "schtasks", "/Create", "/TN", "ShellClawWMISetup", "/TR",
        "powershell.exe -ExecutionPolicy Bypass -File C:\\ShellClawWMISetup.ps1",
        "/SC", "ONCE", "/ST", "00:00", "/RL", "HIGHEST", "/F"
    ], check=True)

    # Run the scheduled task
    subprocess.run(["schtasks", "/Run", "/TN", "ShellClawWMISetup"], check=True)

    # Cleanup
    subprocess.run(["schtasks", "/Delete", "/TN", "ShellClawWMISetup", "/F"], check=True)
    subprocess.run(["del", "C:\\ShellClawWMISetup.ps1"], shell=True, check=True)

    log_detection("✅ WMI subscriptions created via SYSTEM context.")

# Core Detection
import subprocess
from core.forensics import log_detection

def create_wmi_detection():
    """Set up WMI detection with advanced bypass filters and SYSTEM-context logging."""
    log_detection("⚡ Setting up ShellClaw WMI detection...")

    # ⚡ PowerShell script for advanced WMI monitoring
    ps_script = r"""
    $PrimaryLogPath = "C:\Users\Public\ShellClawDetection.log"
    $FallbackLogPath = "C:\Windows\Temp\ShellClawDetection.log"
    try {
        "ShellClaw path test" | Out-File -FilePath $PrimaryLogPath -ErrorAction Stop
        $LogPath = $PrimaryLogPath
    } catch {
        $LogPath = $FallbackLogPath
    }
    Get-WmiObject -Namespace root\subscription -Class __EventFilter | Where-Object { $_.Name -like 'ShellClaw*' } | ForEach-Object { $_.Delete() }
    Get-WmiObject -Namespace root\subscription -Class LogFileEventConsumer | Where-Object { $_.Name -like 'ShellClaw*' } | ForEach-Object { $_.Delete() }
    Get-WmiObject -Namespace root\subscription -Class __FilterToConsumerBinding | Where-Object { $_.Filter -like '*ShellClaw*' } | ForEach-Object { $_.Delete() }
    Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{
        Name = 'ShellClawPSDetection';
        EventNamespace = 'root\cimv2';
        QueryLanguage = 'WQL';
        Query = "SELECT * FROM Win32_ProcessStartTrace WHERE ProcessName='powershell.exe' AND (CommandLine LIKE '%-ep Bypass%' OR CommandLine LIKE '%-nop%' OR CommandLine LIKE '%-EncodedCommand%')"
    }
    $filter = Get-WmiObject -Namespace root\subscription -Class __EventFilter | Where-Object { $_.Name -eq 'ShellClawPSDetection' }
    Set-WmiInstance -Namespace root\subscription -Class LogFileEventConsumer -Arguments @{
        Name = 'ShellClawPSLogConsumer';
        Filename = $LogPath;
        Text = '🚨 [ShellClaw] Suspicious PowerShell execution detected at $(Get-Date)'
    }
    $consumer = Get-WmiObject -Namespace root\subscription -Class LogFileEventConsumer | Where-Object { $_.Name -eq 'ShellClawPSLogConsumer' }
    if ($filter -and $consumer -and $filter.__PATH -and $consumer.__PATH) {
        Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{
            Filter = $filter.__PATH;
            Consumer = $consumer.__PATH
        }
    }
    """

    # 🏃 Execute the PowerShell detection setup
    try:
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", ps_script], check=True)
        log_detection("✅ ShellClaw real-time detection is fully operational.")
    except subprocess.CalledProcessError as e:
        log_detection(f"❌ WMI detection setup failed: {e}")



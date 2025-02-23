# core/hardening.py
from core.utils import run_powershell

def set_execution_policy(policy="AllSigned"):
    """Set PowerShell execution policy securely (requires elevation)."""
    cmd = f"Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy {policy} -Force"
    return run_powershell(cmd, elevate=True)

def enable_logging():
    """Enable critical PowerShell logging for forensics (requires elevation)."""
    cmds = [
        'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\PowerShell\\1\\ShellIds\\Microsoft.PowerShell" -Name "ScriptBlockLogging" -Value @{Enable=$true}',
        'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\PowerShell\\1\\ShellIds\\Microsoft.PowerShell" -Name "ModuleLogging" -Value @{Enable=$true}'
    ]
    return [run_powershell(cmd, elevate=True) for cmd in cmds]

def disable_ps_v2():
    """Disable legacy PowerShell v2 (requires elevation)."""
    return run_powershell("Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root -NoRestart", elevate=True)

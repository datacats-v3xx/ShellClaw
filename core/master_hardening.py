import subprocess
from core.forensics import log_detection
from core.utils import run_powershell

def initialize():
    """Initialize the module."""
    log_detection("✅ Master hardening module loaded successfully.")
    print("✅ Master hardening module initialized.")
    return True

def run_powershell_script(script_path):
    """Run a PowerShell script from a given absolute path."""
    cmd = f'& "{script_path}"'
    return run_powershell(cmd, elevate=True)

def disable_smbv1():
    from core.utils import run_powershell
    return run_powershell("Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force")

def apply_defender_asr_rules():
    from core.utils import run_powershell
    return run_powershell("""
        Set-MpPreference -AttackSurfaceReductionRules_Ids `
        "D4F940AB-401B-4EFC-AADC-AD5F3C50688A","3B576869-A4EC-4529-8536-B80A7769E899" `
        -AttackSurfaceReductionRules_Actions Enabled
    """)

def force_gpo_update():
    from core.utils import run_powershell
    return run_powershell("gpupdate /force")

def run_all():
    """Run all available hardening functions."""
    results = []
    results.append(disable_smbv1())
    results.append(apply_defender_asr_rules())
    results.append(force_gpo_update())
    return "\n".join(results)

# NO PRINT STATEMENT OR CODE EXECUTION AT MODULE LEVEL
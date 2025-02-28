# core/hardening.py
import subprocess


def run_powershell(cmd):
    """Run PowerShell silently."""
    try:
        result = subprocess.run(
            ["powershell", "-WindowStyle", "Hidden", "-ExecutionPolicy", "Bypass", "-Command", cmd],
            capture_output=True, text=True, check=True
        )
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip()}


def set_execution_policy(policy="AllSigned"):
    return run_powershell(f"Set-ExecutionPolicy {policy} -Scope LocalMachine -Force")


def enable_logging():
    """Enable PowerShell logging by ensuring registry paths exist first."""
    from core.utils import run_powershell
    results = []

    # PS script to create registry paths if missing and set logging
    ps_script = """
    $scriptBlockPath = 'HKLM:\\Software\\Policies\\Microsoft\\Windows\\PowerShell\\ScriptBlockLogging'
    $transcriptionPath = 'HKLM:\\Software\\Policies\\Microsoft\\Windows\\PowerShell\\Transcription'

    # Ensure ScriptBlockLogging path exists
    if (-not (Test-Path $scriptBlockPath)) {
        New-Item -Path $scriptBlockPath -Force
    }
    Set-ItemProperty -Path $scriptBlockPath -Name 'EnableScriptBlockLogging' -Value 1
    Set-ItemProperty -Path $scriptBlockPath -Name 'EnableScriptBlockInvocationLogging' -Value 1

    # Ensure Transcription path exists
    if (-not (Test-Path $transcriptionPath)) {
        New-Item -Path $transcriptionPath -Force
    }
    Set-ItemProperty -Path $transcriptionPath -Name 'EnableTranscripting' -Value 1
    Set-ItemProperty -Path $transcriptionPath -Name 'OutputDirectory' -Value 'C:\\Windows\\Temp\\PS_Transcripts'
    """

    # Execute PS and return results
    result = run_powershell(ps_script)
    results.append(result)
    return results


def disable_ps_v2():
    return run_powershell('Disable-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2Root -NoRestart')

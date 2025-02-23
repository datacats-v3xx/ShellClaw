# Core utilities
import subprocess

def run_powershell(cmd, elevate=False):
    """Run PowerShell commands with optional elevation."""
    try:
        if elevate:
            # Wrap cmd in escaped double quotes for proper argument parsing
            elevated_cmd = f'Start-Process powershell -Verb RunAs -ArgumentList \'-Command "{cmd}"\''
            result = subprocess.run(["powershell", "-Command", elevated_cmd],
                                    capture_output=True, text=True, check=True)
        else:
            result = subprocess.run(["powershell", "-Command", cmd],
                                    capture_output=True, text=True, check=True)

        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip()}


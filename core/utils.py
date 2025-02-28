# core/utils.py - Safer PowerShell execution
import subprocess


def run_powershell(cmd, elevate=False):
    """Run PowerShell command with improved safety."""
    try:
        if elevate:
            # command construction for elevation
            full_cmd = [
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-Command",
                f"Start-Process powershell -Verb runAs -ArgumentList '-ExecutionPolicy', 'Bypass', '-Command', \"{cmd.replace('\"', '`\"')}\""
            ]
        else:
            # non-elevated execution
            full_cmd = [
                "powershell",
                "-ExecutionPolicy", "Bypass",
                "-Command",
                cmd
            ]

        # limited output capture
        proc = subprocess.Popen(
            full_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )

        # Limit output size to prevent buffer issues
        stdout, stderr = proc.communicate(timeout=30)

        return {
            "success": proc.returncode == 0,
            "output": stdout[:10000] if stdout else "",  # Limit output size
            "error": stderr[:10000] if stderr else "",  # Limit error size
            "returncode": proc.returncode
        }

    except subprocess.TimeoutExpired:
        proc.kill()
        return {"success": False, "error": "Command timed out", "returncode": -1}
    except Exception as e:
        return {"success": False, "error": str(e)[:10000], "returncode": -1}
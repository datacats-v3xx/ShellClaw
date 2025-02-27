# core/forensics.py - Fixed version
import os
import sys
from datetime import datetime
import subprocess

# Base path function defined once
def get_base_path():
    """Handle PyInstaller's temp path vs. local execution."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # If bundled by PyInstaller
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # For direct execution

# Log directory function defined once
def ensure_log_directory():
    """Ensure log directory exists."""
    log_dir = os.path.join(get_base_path(), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

# Single consistent log path
LOG_PATH = os.path.join(ensure_log_directory(), "shellclaw_log.txt")

def log_detection(message):
    """Log detection events to file."""
    entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(entry)

def get_detection_logs():
    """Return detection logs for UI display."""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as file:
            return file.read()
    return "🚫 No detections logged yet."

def clear_detection_logs():
    """Clear the detection log file."""
    if os.path.exists(LOG_PATH):
        open(LOG_PATH, "w").close()

def parse_defender_logs():
    """Parse recent Defender logs and push them to the UI."""
    cmd = 'Get-WinEvent -LogName "Microsoft-Windows-Windows Defender/Operational" | Select-Object -First 5 | Format-List'
    try:
        result = subprocess.run(["powershell", "-Command", cmd], 
                               capture_output=True, text=True, timeout=10)
        log_detection(f"🛡️ Defender Logs:\n{result.stdout}")
        return result.stdout
    except Exception as e:
        log_detection(f"❌ Error getting Defender logs: {str(e)}")
        return f"Error: {str(e)}"
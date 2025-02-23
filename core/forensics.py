# core/forensics.py
import os
from datetime import datetime
import sys

def get_base_path():
    """Handle PyInstaller's temp path vs. local execution."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)  # If bundled by PyInstaller
    return os.path.dirname(os.path.abspath(__file__))  # For direct execution

def log_detection(message):
    base_path = get_base_path()
    log_dir = os.path.join(base_path, "logs")
    log_file = os.path.join(log_dir, "shellclaw_log.txt")

    # ✅ Auto-create 'logs' directory if missing
    os.makedirs(log_dir, exist_ok=True)

    # 📝 Append logs safely
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")

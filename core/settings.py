# Create core/settings.py
import json
import os

DEFAULT_SETTINGS = {
    "dark_mode": False,
    "auto_refresh_logs": True,
    "refresh_interval": 5000,  # milliseconds
    "default_hardening": [
        "execution_policy",
        "ps_logging",
        "disable_v2"
    ],
    "log_path": "logs/shellclaw_log.txt"
}

def get_settings_path():
    """Get path to settings file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "settings.json")

def load_settings():
    """Load settings from file or return defaults."""
    try:
        path = get_settings_path()
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return DEFAULT_SETTINGS
    except Exception as e:
        print(f"Error loading settings: {e}")
        return DEFAULT_SETTINGS

def save_settings(settings):
    """Save settings to file."""
    try:
        path = get_settings_path()
        with open(path, "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False
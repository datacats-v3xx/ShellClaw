# Create ui/settings_tab.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QCheckBox,
                             QPushButton, QSpinBox, QLabel, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from core.settings import load_settings, save_settings


class SettingsTab(QWidget):
    settings_changed = pyqtSignal()  # Signal when settings change

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Load current settings
        self.settings = load_settings()

        # Create form layout
        form = QFormLayout()

        # UI Settings group
        ui_group = QGroupBox("UI Settings")
        ui_layout = QFormLayout()

        self.dark_mode = QCheckBox()
        self.dark_mode.setChecked(self.settings.get("dark_mode", False))
        ui_layout.addRow("Dark Mode:", self.dark_mode)

        self.auto_refresh = QCheckBox()
        self.auto_refresh.setChecked(self.settings.get("auto_refresh_logs", True))
        ui_layout.addRow("Auto-refresh Logs:", self.auto_refresh)

        self.refresh_interval = QSpinBox()
        self.refresh_interval.setRange(1000, 60000)
        self.refresh_interval.setSingleStep(1000)
        self.refresh_interval.setValue(self.settings.get("refresh_interval", 5000))
        self.refresh_interval.setSuffix(" ms")
        ui_layout.addRow("Refresh Interval:", self.refresh_interval)

        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)

        # Default Hardening Settings
        hardening_group = QGroupBox("Default Hardening Options")
        hardening_layout = QVBoxLayout()

        default_hardening = self.settings.get("default_hardening", [])

        self.exec_policy = QCheckBox("Set Execution Policy")
        self.exec_policy.setChecked("execution_policy" in default_hardening)
        hardening_layout.addWidget(self.exec_policy)

        self.ps_logging = QCheckBox("Enable PowerShell Logging")
        self.ps_logging.setChecked("ps_logging" in default_hardening)
        hardening_layout.addWidget(self.ps_logging)

        self.disable_v2 = QCheckBox("Disable PowerShell v2")
        self.disable_v2.setChecked("disable_v2" in default_hardening)
        hardening_layout.addWidget(self.disable_v2)

        self.wmi_detection = QCheckBox("Activate WMI Detection")
        self.wmi_detection.setChecked("wmi_detection" in default_hardening)
        hardening_layout.addWidget(self.wmi_detection)

        hardening_group.setLayout(hardening_layout)
        layout.addWidget(hardening_group)

        # Save button
        save_button = QPushButton("💾 Save Settings")
        save_button.clicked.connect(self.save_current_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def apply_settings(self):
        """Apply settings from settings tab."""
        try:
            from core.settings import load_settings
            settings = load_settings()

            # ✅ Fixed the dark mode reference
            self.settings_tab.dark_mode.setChecked(settings.get("dark_mode", False))

            # Apply log refresh settings
            refresh_interval = settings.get("refresh_interval", 5000)
            self.log_timer.setInterval(refresh_interval)

            if not settings.get("auto_refresh_logs", True):
                self.log_timer.stop()
            else:
                self.log_timer.start()

            # Apply default hardening options
            default_hardening = settings.get("default_hardening", [])
            self.execution_policy_checkbox.setChecked("execution_policy" in default_hardening)
            self.ps_logging_checkbox.setChecked("ps_logging" in default_hardening)
            self.disable_v2_checkbox.setChecked("disable_v2" in default_hardening)
            self.wmi_detection_checkbox.setChecked("wmi_detection" in default_hardening)

            self.output_console.append("✅ Settings applied")
        except Exception as e:
            self.output_console.append(f"Error applying settings: {str(e)}")

    def save_current_settings(self):
        """Save current settings to file."""
        # Update settings from UI
        self.settings["dark_mode"] = self.dark_mode.isChecked()
        self.settings["auto_refresh_logs"] = self.auto_refresh.isChecked()
        self.settings["refresh_interval"] = self.refresh_interval.value()

        # Update default hardening options
        default_hardening = []
        if self.exec_policy.isChecked():
            default_hardening.append("execution_policy")
        if self.ps_logging.isChecked():
            default_hardening.append("ps_logging")
        if self.disable_v2.isChecked():
            default_hardening.append("disable_v2")
        if self.wmi_detection.isChecked():
            default_hardening.append("wmi_detection")

        self.settings["default_hardening"] = default_hardening

        # Save to file
        if save_settings(self.settings):
            # Emit signal to notify main UI
            self.settings_changed.emit()
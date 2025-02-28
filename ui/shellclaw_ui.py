from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QCheckBox, QPushButton, QLabel,
    QTabWidget, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from core.forensics import log_detection, get_detection_logs, clear_detection_logs
from core.threads import PowerShellWorker, HardeningWorker


class ShellClawUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShellClaw: Endpoint Defense - Manual Mode")
        self.resize(800, 600)

        # ✅ Output Console
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)

        # 💡 Main Layout
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.addWidget(self.output_console)

        self.output_console.append("✅ ShellClawUI Initialized")
        log_detection("✅ ShellClawUI Initialized")

        # 💡 Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # 💡 Schedule deferred initialization
        QTimer.singleShot(100, self.deferred_initialization)

    def deferred_initialization(self):
        """Initialize components after UI is loaded."""
        self.output_console.append("💬 Loading additional components...")

        self.create_hardening_tab()
        self.create_logs_tab()
        self.add_master_tab()
        self.add_process_tab()
        self.add_settings_tab()

        self.output_console.append("✅ Application fully initialized.")

    def create_hardening_tab(self):
        """🛡️ Create Hardening Controls tab."""
        self.hardening_tab = QWidget()
        self.tabs.addTab(self.hardening_tab, "🛡️ Hardening Controls")
        hardening_layout = QVBoxLayout(self.hardening_tab)

        # Select All Checkbox
        self.select_all_checkbox = QCheckBox("✅ Select All")
        self.select_all_checkbox.stateChanged.connect(self.toggle_all_hardening)
        hardening_layout.addWidget(self.select_all_checkbox)

        # Individual Hardening Options
        self.execution_policy_checkbox = QCheckBox("🔒 Set Execution Policy (AllSigned)")
        self.ps_logging_checkbox = QCheckBox("📝 Enable PowerShell Logging")
        self.disable_v2_checkbox = QCheckBox("🛡️ Disable PowerShell v2")
        self.wmi_detection_checkbox = QCheckBox("⚡ Activate WMI Detection")

        for cb in [self.execution_policy_checkbox, self.ps_logging_checkbox,
                   self.disable_v2_checkbox, self.wmi_detection_checkbox]:
            hardening_layout.addWidget(cb)

        # Run Hardening Button
        self.run_button = QPushButton("🚀 Run Selected Hardening")
        self.run_button.clicked.connect(self.run_selected_hardening)
        hardening_layout.addWidget(self.run_button)

    def create_logs_tab(self):
        """📜 Create Detection Logs tab."""
        self.logs_tab = QWidget()
        self.tabs.addTab(self.logs_tab, "📜 Detection Logs")
        logs_layout = QVBoxLayout(self.logs_tab)

        self.logs_console = QTextEdit()
        self.logs_console.setReadOnly(True)
        logs_layout.addWidget(self.logs_console)

        # Refresh & Clear buttons
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Refresh Logs")
        refresh_btn.clicked.connect(self.refresh_logs)
        clear_btn = QPushButton("🧹 Clear Logs")
        clear_btn.clicked.connect(self.clear_logs)
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(clear_btn)
        logs_layout.addLayout(button_layout)

        # Auto-refresh logs every 5 seconds
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.refresh_logs)
        self.log_timer.start(5000)

    def add_master_tab(self):
        """🛡️ Master Hardening Tab."""
        try:
            from ui.master_script_tab import MasterScriptTab
            self.master_tab = MasterScriptTab()
            self.tabs.addTab(self.master_tab, "🛡️ Master Hardening")
        except Exception as e:
            self.output_console.append(f"⚠️ Error loading Master Hardening tab: {str(e)}")

    def add_process_tab(self):
        """👁️ Process Monitor Tab."""
        try:
            from ui.process_monitor_tab import ProcessMonitorTab
            self.process_tab = ProcessMonitorTab()
            self.tabs.addTab(self.process_tab, "👁️ Process Monitor")
        except Exception as e:
            self.output_console.append(f"⚠️ Error loading Process Monitor tab: {str(e)}")

    def add_settings_tab(self):
        """⚙️ Settings Tab."""
        try:
            from ui.settings_tab import SettingsTab
            self.settings_tab = SettingsTab()
            self.settings_tab.settings_changed.connect(self.apply_settings)
            self.tabs.addTab(self.settings_tab, "⚙️ Settings")
        except Exception as e:
            self.output_console.append(f"⚠️ Error loading Settings tab: {str(e)}")

    def toggle_all_hardening(self, state):
        """✅ Toggle all checkboxes."""
        check = state == Qt.Checked
        self.execution_policy_checkbox.setChecked(check)
        self.ps_logging_checkbox.setChecked(check)
        self.disable_v2_checkbox.setChecked(check)
        self.wmi_detection_checkbox.setChecked(check)

    def run_selected_hardening(self):
        """⚡ Run hardening tasks in background."""
        self.output_console.append("🚀 Running selected hardening...")
        operations = []

        if self.execution_policy_checkbox.isChecked():
            from core.hardening import set_execution_policy
            operations.append(("Set Execution Policy", lambda: set_execution_policy("AllSigned")))

        if self.ps_logging_checkbox.isChecked():
            from core.hardening import enable_logging
            operations.append(("Enable PowerShell Logging", enable_logging))

        if self.disable_v2_checkbox.isChecked():
            from core.hardening import disable_ps_v2
            operations.append(("Disable PowerShell v2", disable_ps_v2))

        if self.wmi_detection_checkbox.isChecked():
            from core.detection import create_wmi_detection
            operations.append(("Activate WMI Detection", create_wmi_detection))

        # Run in thread
        self.hardening_worker = HardeningWorker(operations)
        self.hardening_worker.progress.connect(self.update_hardening_progress)
        self.hardening_worker.finished.connect(self.hardening_completed)
        self.hardening_worker.start()

    def update_hardening_progress(self, message, percentage):
        """📈 Update progress."""
        self.output_console.append(message)

    def hardening_completed(self):
        """✅ Hardening completed."""
        self.output_console.append("🎯 Hardening process completed successfully.")

    def refresh_logs(self):
        """🔄 Refresh logs."""
        try:
            logs = get_detection_logs()
            self.logs_console.setPlainText(logs)
        except Exception as e:
            self.output_console.append(f"⚠️ Error refreshing logs: {str(e)}")

    def clear_logs(self):
        """🧹 Clear logs."""
        try:
            clear_detection_logs()
            self.logs_console.setPlainText("")
            self.output_console.append("🧹 Detection logs cleared.")
        except Exception as e:
            self.output_console.append(f"⚠️ Error clearing logs: {str(e)}")

    def apply_settings(self):
        """Apply settings from settings tab."""
        try:
            from core.settings import load_settings
            settings = load_settings()

            # Corrected the checkbox reference
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

            self.output_console.append("Settings applied")
        except Exception as e:
            self.output_console.append(f" Error applying settings: {str(e)}")

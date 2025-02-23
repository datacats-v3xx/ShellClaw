from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel,
    QPushButton, QCheckBox, QTextEdit, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import sys, qdarkstyle
from core.hardening import set_execution_policy, enable_logging, disable_ps_v2
from core.forensics import log_detection


class ShellClawUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐾 ShellClaw: PowerShell Defense Engine")
        self.setGeometry(400, 100, 900, 600)

        tabs = QTabWidget()
        tabs.addTab(self.personal_tab_ui(), "🏠 Personal")
        tabs.addTab(self.professional_tab_ui(), "🏢 Professional")
        tabs.addTab(self.detection_tab_ui(), "⚡ Live Detection")
        tabs.addTab(self.logs_tab_ui(), "📝 Audit Logs")
        self.setCentralWidget(tabs)

        # 🌑 Dark Mode toggle
        dark_mode_btn = QPushButton("🌙 Toggle Dark Mode")
        dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        self.statusBar().addPermanentWidget(dark_mode_btn)

    # 🏠 PERSONAL MODE
    def personal_tab_ui(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🏠 **Personal Mode**: Maximum hardening for home environments."))

        self.p_exec_policy = QCheckBox("🔒 Set Execution Policy: AllSigned")
        self.p_exec_policy.stateChanged.connect(lambda: self.toggle_setting(set_execution_policy, "AllSigned"))
        layout.addWidget(self.p_exec_policy)

        self.p_logging = QCheckBox("📝 Enable PowerShell Logging")
        self.p_logging.stateChanged.connect(lambda: self.toggle_setting(enable_logging))
        layout.addWidget(self.p_logging)

        self.p_disable_v2 = QCheckBox("🛡️ Disable PowerShell v2")
        self.p_disable_v2.stateChanged.connect(lambda: self.toggle_setting(disable_ps_v2))
        layout.addWidget(self.p_disable_v2)

        secure_btn = QPushButton("☑️ Apply All (Personal)")
        secure_btn.clicked.connect(self.apply_personal_mode)
        layout.addWidget(secure_btn)

        tab.setLayout(layout)
        return tab

    # 🏢 PROFESSIONAL MODE
    def professional_tab_ui(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🏢 **Professional Mode**: Balanced hardening for enterprise compatibility."))

        self.pro_exec_policy = QCheckBox("🔒 Set Execution Policy: RemoteSigned")
        self.pro_exec_policy.stateChanged.connect(lambda: self.toggle_setting(set_execution_policy, "RemoteSigned"))
        layout.addWidget(self.pro_exec_policy)

        self.pro_logging = QCheckBox("📝 Enable Module & ScriptBlock Logging")
        self.pro_logging.stateChanged.connect(lambda: self.toggle_setting(enable_logging))
        layout.addWidget(self.pro_logging)

        secure_btn = QPushButton("☑️ Apply All (Professional)")
        secure_btn.clicked.connect(self.apply_professional_mode)
        layout.addWidget(secure_btn)

        tab.setLayout(layout)
        return tab

    # ⚡ LIVE DETECTION TAB
    def detection_tab_ui(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.live_log = QTextEdit()
        self.live_log.setReadOnly(True)
        layout.addWidget(QLabel("⚡ **Live Bypass Detection:** Real-time alerts for suspicious PowerShell execution."))
        layout.addWidget(self.live_log)
        tab.setLayout(layout)
        return tab

    # 📝 AUDIT LOG TAB
    def logs_tab_ui(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.audit_logs = QTextEdit()
        self.audit_logs.setReadOnly(True)

        load_logs_btn = QPushButton("🔄 Refresh Logs")
        load_logs_btn.clicked.connect(self.load_logs)

        export_btn = QPushButton("📁 Export Logs")
        export_btn.clicked.connect(self.export_logs)

        layout.addWidget(QLabel("📝 **Audit Logs:** Review and export detection history."))
        layout.addWidget(self.audit_logs)
        layout.addWidget(load_logs_btn)
        layout.addWidget(export_btn)
        tab.setLayout(layout)
        return tab

    # 💡 FUNCTIONALITY
    def toggle_setting(self, func, arg=None):
        """Toggle individual hardening features."""
        if arg:
            func(arg)
        else:
            func()
        log_detection(f"✅ Setting applied: {func.__name__}")

    def apply_personal_mode(self):
        """Apply all personal settings at once."""
        self.p_exec_policy.setChecked(True)
        self.p_logging.setChecked(True)
        self.p_disable_v2.setChecked(True)
        log_detection("🏠 ✅ Personal Mode: All settings applied.")

    def apply_professional_mode(self):
        """Apply all professional settings at once."""
        self.pro_exec_policy.setChecked(True)
        self.pro_logging.setChecked(True)
        log_detection("🏢 ✅ Professional Mode: All settings applied.")

    def load_logs(self):
        """Load detection logs into UI."""
        try:
            with open("logs/shellclaw_log.txt", "r", encoding="utf-8") as f:
                self.audit_logs.setText(f.read())
        except FileNotFoundError:
            self.audit_logs.setText("❌ No logs found.")

    def export_logs(self):
        """Export logs to user-chosen path."""
        filename, _ = QFileDialog.getSaveFileName(self, "Save Logs As", "", "Text Files (*.txt)")
        if filename:
            with open(filename, "w", encoding="utf-8") as f_out, open("logs/shellclaw_log.txt", "r", encoding="utf-8") as f_in:
                f_out.write(f_in.read())
            QMessageBox.information(self, "✅ Export Successful", f"Logs exported to:\n{filename}")

    def toggle_dark_mode(self):
        """Switch between light and dark modes."""
        app = QApplication.instance()
        if app.styleSheet():
            app.setStyleSheet("")
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


# 🚀 Launch UI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # Default to dark mode
    window = ShellClawUI()
    window.show()
    sys.exit(app.exec_())

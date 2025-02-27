from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel


# Import functions only when needed
class MasterScriptTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)

        # Buttons for each function
        smb_btn = QPushButton("Disable SMBv1")
        asr_btn = QPushButton("Apply Defender ASR Rules")
        gpo_btn = QPushButton("Force GPO Update")
        all_btn = QPushButton("🛡️ Run All Hardening Steps")

        # Use lazy imports in the button handlers
        smb_btn.clicked.connect(self.run_disable_smbv1)
        asr_btn.clicked.connect(self.run_apply_asr_rules)
        gpo_btn.clicked.connect(self.run_force_gpo)
        all_btn.clicked.connect(self.run_all)

        # Add widgets
        layout.addWidget(QLabel("📝 Select hardening tasks to run:"))
        layout.addWidget(smb_btn)
        layout.addWidget(asr_btn)
        layout.addWidget(gpo_btn)
        layout.addWidget(all_btn)
        layout.addWidget(QLabel("🔍 Status Output:"))
        layout.addWidget(self.status_log)
        self.setLayout(layout)

    def run_disable_smbv1(self):
        from core.master_hardening import disable_smbv1
        output = disable_smbv1()
        self.status_log.append(output)

    def run_apply_asr_rules(self):
        from core.master_hardening import apply_defender_asr_rules
        output = apply_defender_asr_rules()
        self.status_log.append(output)

    def run_force_gpo(self):
        from core.master_hardening import force_gpo_update
        output = force_gpo_update()
        self.status_log.append(output)

    def run_all(self):
        """Run all hardening tasks (BitLocker removed)."""
        self.status_log.append("⚡ Running all hardening steps (BitLocker excluded)...")
        from core.master_hardening import disable_smbv1, apply_defender_asr_rules, force_gpo_update
        for func in [disable_smbv1, apply_defender_asr_rules, force_gpo_update]:
            output = func()
            self.status_log.append(output)
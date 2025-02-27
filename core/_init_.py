# 💾 Detection Logs Tab
self.logs_tab = QWidget()
self.tabs.addTab(self.logs_tab, "📝 Detection Logs")
logs_layout = QVBoxLayout()
self.logs_tab.setLayout(logs_layout)

self.logs_console = QTextEdit()
self.logs_console.setReadOnly(True)
logs_layout.addWidget(self.logs_console)

self.refresh_logs_button = QPushButton("🔄 Refresh Logs")
self.refresh_logs_button.clicked.connect(self.refresh_logs)
logs_layout.addWidget(self.refresh_logs_button)

self.clear_logs_button = QPushButton("🧹 Clear Logs")
self.clear_logs_button.clicked.connect(self.clear_logs)
logs_layout.addWidget(self.clear_logs_button)

# ⏱️ Auto-refresh every 5s
self.log_timer = QTimer(self)
self.log_timer.timeout.connect(self.refresh_logs)
self.log_timer.start(5000)  # every 5 seconds

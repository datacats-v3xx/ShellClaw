from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget,
    QTreeWidgetItem, QPushButton, QLabel
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor  # Ensure this import is present
from core.threads import ProcessListWorker  # Import here for clarity


class ProcessMonitorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Process display tree
        self.process_tree = QTreeWidget()
        self.process_tree.setHeaderLabels(["PID", "Name", "CPU %", "Memory (MB)", "Command Line"])
        self.process_tree.setAlternatingRowColors(True)

        # Refresh button (corrected to self.refresh_button)
        self.refresh_button = QPushButton("🔄 Refresh Processes")
        self.refresh_button.clicked.connect(self.refresh_processes)

        # Add widgets to layout
        layout.addWidget(QLabel("👁️ Running Processes:"))
        layout.addWidget(self.process_tree)
        layout.addWidget(self.refresh_button)  # Updated reference

        self.setLayout(layout)

        # Auto-refresh timer
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_processes)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds

        # Initial load
        self.refresh_processes()

    def refresh_processes(self):
        """Start process refresh in background thread."""
        # Disable refresh button during loading
        self.refresh_button.setEnabled(False)
        self.refresh_button.setText("Refreshing...")

        # Worker thread for process fetching
        self.worker = ProcessListWorker()
        self.worker.finished.connect(self.update_process_list)
        self.worker.start()

    def update_process_list(self, processes):
        """Update UI with processes from worker thread."""
        self.process_tree.clear()

        for process in processes:
            item = QTreeWidgetItem([
                str(process['pid']),
                process['name'],
                str(process['cpu']),
                str(process['memory']),
                process['command_line'] or "N/A"
            ])

            # Highlight PowerShell processes
            if "powershell" in process['name'].lower():
                for i in range(5):
                    item.setBackground(i, QColor(255, 200, 200))

            self.process_tree.addTopLevelItem(item)

        # Auto-resize columns
        for i in range(5):
            self.process_tree.resizeColumnToContents(i)

        # Re-enable refresh button
        self.refresh_button.setEnabled(True)
        self.refresh_button.setText("🔄 Refresh Processes")

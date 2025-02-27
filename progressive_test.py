# progressive_test.py - Progressive testing of application components
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget, QTextEdit)


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShellClaw Test")
        self.setGeometry(100, 100, 600, 400)

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Output console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.layout.addWidget(self.console)

        # Test buttons
        self.add_test_buttons()

        # Log initialization
        self.log("Test window initialized")

    def log(self, message):
        """Add message to console."""
        self.console.append(message)
        print(message)

    def add_test_buttons(self):
        """Add test buttons for different components."""
        # Basic PowerShell test
        ps_button = QPushButton("Test PowerShell")
        ps_button.clicked.connect(self.test_powershell)
        self.layout.addWidget(ps_button)

        # File system test
        fs_button = QPushButton("Test File System")
        fs_button.clicked.connect(self.test_filesystem)
        self.layout.addWidget(fs_button)

        # Settings test
        settings_button = QPushButton("Test Settings")
        settings_button.clicked.connect(self.test_settings)
        self.layout.addWidget(settings_button)

    def test_powershell(self):
        """Test basic PowerShell functionality."""
        self.log("Testing PowerShell...")
        try:
            import subprocess
            result = subprocess.run(
                ["powershell", "-Command", "Write-Host 'PowerShell test'"],
                capture_output=True, text=True, timeout=5
            )
            self.log(f"PowerShell output: {result.stdout}")
        except Exception as e:
            self.log(f"PowerShell error: {str(e)}")

    def test_filesystem(self):
        """Test file system operations."""
        self.log("Testing file system...")
        try:
            if not os.path.exists("logs"):
                os.makedirs("logs")
            with open("logs/test.log", "w") as f:
                f.write("Test log entry\n")
            self.log("File system test successful")
        except Exception as e:
            self.log(f"File system error: {str(e)}")

    def test_settings(self):
        """Test settings functionality."""
        self.log("Testing settings...")
        try:
            from core.settings import load_settings
            settings = load_settings()
            self.log(f"Settings loaded: {settings}")
        except Exception as e:
            self.log(f"Settings error: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        print(traceback.format_exc())
# core/threads.py
from PyQt5.QtCore import QThread, pyqtSignal
from core.utils import run_powershell

class ProcessListWorker(QThread):
    finished = pyqtSignal(list)

    def watch_ps_scripts(watch_dir="C:\\Users\\Public\\"):
        import time
        import os
        print(f"👀 Watching directory: {watch_dir}")
        tracked = set(os.listdir(watch_dir))
        while True:
            time.sleep(5)  # Keep thread alive
            current = set(os.listdir(watch_dir))
            new_files = current - tracked
            if new_files:
                print(f"🚨 Detected new files: {new_files}")
            tracked = current

    def run(self):
        import subprocess
        import csv
        from io import StringIO

        try:
            # PowerShell command to get processes with details
            ps_command = """
            Get-Process | Select-Object Id, ProcessName, CPU, 
            @{Name="Memory(MB)";Expression={[math]::Round($_.WorkingSet64 / 1MB, 2)}}, 
            @{Name="CommandLine";Expression={
                (Get-CimInstance -Class Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
            }} | ConvertTo-Csv -NoTypeInformation
            """

            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True, text=True, check=True
            )

            # Parse CSV output
            processes = []
            csv_reader = csv.reader(StringIO(result.stdout))
            next(csv_reader)  # Skip header

            for row in csv_reader:
                if len(row) >= 5:
                    processes.append({
                        'pid': row[0],
                        'name': row[1],
                        'cpu': row[2],
                        'memory': row[3],
                        'command_line': row[4]
                    })

            self.finished.emit(processes)

        except Exception as e:
            print(f"Error fetching processes: {e}")
            self.finished.emit([])

class PowerShellWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        result = run_powershell(self.command)
        self.finished.emit(result)


class HardeningWorker(QThread):
    progress = pyqtSignal(str, int)
    finished = pyqtSignal()

    def __init__(self, options):
        super().__init__()
        self.options = options

    def run(self):
        # Process hardening options in sequence
        total = len(self.options)
        for i, (name, func) in enumerate(self.options):
            self.progress.emit(f"Running {name}...", int((i / total) * 100))
            # Run the hardening function
            result = func()
            # Report progress
            self.progress.emit(f"Completed {name}: {result}", int(((i + 1) / total) * 100))

        self.finished.emit()

    if __name__ == "__main__":
        print("🧵 Starting thread tests...")  # Debug print to confirm execution
        # Example thread start
        from core.detection import watch_ps_scripts
        import threading

        t = threading.Thread(target=watch_ps_scripts, daemon=True)
        t.start()
        t.join()  # Keep script alive for the thread to run

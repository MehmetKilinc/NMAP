import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QProgressBar, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt

class NmapScanner(QThread):
    progress_update = pyqtSignal(int)
    scan_result = pyqtSignal(str)

    def __init__(self, target_ip):
        super().__init__()
        self.target_ip = target_ip

    def run(self):
        nmap_process = subprocess.Popen(['nmap', '-F', self.target_ip], stdout=subprocess.PIPE)
        output, error = nmap_process.communicate()
        self.scan_result.emit(output.decode())
        self.progress_update.emit(100)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nmap Scanner')
        self.resize(400, 300)

        self.target_ip_label = QLabel('Target IP:')
        self.target_ip_input = QTextEdit()
        self.target_ip_input.setPlaceholderText('Enter target IP')

        self.scan_button = QPushButton('Scan')
        self.scan_button.clicked.connect(self.start_scan)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.result_label = QLabel('Scan Result:')
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.target_ip_label)
        layout.addWidget(self.target_ip_input)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

    def start_scan(self):
        target_ip = self.target_ip_input.toPlainText().strip()
        if not target_ip:
            return
        self.progress_bar.setValue(0)
        self.result_text.clear()
        self.scan_thread = NmapScanner(target_ip)
        self.scan_thread.progress_update.connect(self.update_progress)
        self.scan_thread.scan_result.connect(self.show_result)
        self.scan_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def show_result(self, result):
        self.result_text.setText(result)
        self.progress_bar.setValue(100)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

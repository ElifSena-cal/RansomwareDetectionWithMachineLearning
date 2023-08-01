import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QLineEdit, QLabel, QFileDialog, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import subprocess

class AnalysisThread(QThread):
    progressUpdated = pyqtSignal(int)
    analysisFinished = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        output = subprocess.run(['python', 'request.py', self.file_path], capture_output=True, text=True)
        self.analysisFinished.emit(output.stdout)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Ransomware Detection'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout(self)

        self.label = QLabel('Selected File:', self)
        layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        browse_btn = QPushButton('Browse', self)
        browse_btn.setToolTip('Select File')
        layout.addWidget(browse_btn)
        browse_btn.clicked.connect(self.browse_files)

        analyze_btn = QPushButton('Analyze', self)
        analyze_btn.setToolTip('Analyze File')
        layout.addWidget(analyze_btn)
        analyze_btn.clicked.connect(self.analyze_file)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.output_label = QLabel('Output:', self)
        layout.addWidget(self.output_label)

        self.output_textbox = QTextEdit(self)
        layout.addWidget(self.output_textbox)
        self.output_textbox.setReadOnly(True)

        self.setLayout(layout)
        self.show()

    def browse_files(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File', 'c:\\', 'Executable files (*.exe)')
        self.textbox.setText(file_path)

    def analyze_file(self):
        file_path = self.textbox.text()

        if not file_path:
            return

        self.progress_bar.setValue(0)
        self.progress_bar.setFormat('Analyzing...')

        self.analysis_thread = AnalysisThread(file_path)
        self.analysis_thread.progressUpdated.connect(self.update_progress)
        self.analysis_thread.analysisFinished.connect(self.display_output)
        self.analysis_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_output(self, output):
        self.progress_bar.setFormat('Analysis Complete')
        self.output_textbox.setText(output)

class AnalysisThread(QThread):
    progressUpdated = pyqtSignal(int)
    analysisFinished = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        # Simulating analysis process
        total_steps = 10

        for step in range(1, total_steps + 1):
            progress = int((step / total_steps) * 100)
            self.progressUpdated.emit(progress)
            self.msleep(500)  # Simulating time-consuming step

        output = subprocess.run(['python', 'request.py', self.file_path], capture_output=True, text=True)
        self.analysisFinished.emit(output.stdout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

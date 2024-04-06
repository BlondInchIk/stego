import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QFileDialog, QTextEdit, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Steganography App")
        self.setMinimumSize(800, 400)

        self.algorithm_label = QLabel("Choose algorithm:", self)
        self.algorithm_label.move(50, 50)

        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.move(200, 50)
        self.algorithm_combo.addItem("S-UNIWARD")
        # self.algorithm_combo.addItem("Algorithm 2")

        self.input_file_button = QPushButton("Select Input File", self)
        self.input_file_button.move(50, 100)
        self.input_file_button.clicked.connect(self.select_input_file)

        self.input_file_label = QLabel("Input file name:", self)
        self.input_file_label.move(200, 105)
        self.input_file_label.setWordWrap(True)

        self.output_file_label = QLabel("Output file name:", self)
        self.output_file_label.move(50, 150)

        self.output_file_edit = QLineEdit(self)
        self.output_file_edit.setGeometry(200, 150, 300, 30)

        self.data_file_button = QPushButton("Select Data File", self)
        self.data_file_button.move(50, 200)
        self.data_file_button.clicked.connect(self.select_data_file)

        self.data_file_label = QLabel("Data file name:", self)
        self.data_file_label.move(200, 205)
        self.data_file_label.setWordWrap(True)

        self.steganography_button = QPushButton("Run Steganography", self)
        self.steganography_button.move(50, 250)
        self.steganography_button.clicked.connect(self.run_steganography)

        self.reverse_steganography_button = QPushButton("Run Reverse Steganography", self)
        self.reverse_steganography_button.move(220, 250)
        self.reverse_steganography_button.clicked.connect(self.run_reverse_steganography)

        self.log_label = QLabel("Log:", self)
        self.log_label.move(400, 50)

        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setGeometry(400, 80, 350, 300)
        self.log_text_edit.setReadOnly(True)
        

    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if file_name:
            self.input_file_label.setText(file_name)

    def select_data_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Data File", filter="Text Files (*.txt)")
        if file_name:
            self.data_file_label.setText(file_name)

    def run_steganography(self):
        algorithm = self.algorithm_combo.currentText()
        input_file = self.input_file_label.text()
        output_file = self.output_file_edit.text()
        data_file = self.data_file_label.text()
        
        algorithm_file = algorithm + ".py"
        
        if algorithm not in ["S-UNIWARD"]:
            QMessageBox.warning(self, "Error", "Invalid algorithm selected.")
            return
        
        if not input_file.endswith(".bmp"):
            QMessageBox.warning(self, "Error", "Input file must be in BMP format.")
            return

        if not data_file.endswith(".txt"):
            QMessageBox.warning(self, "Error", "Data file must be in TXT format.")
            return
        
        command = "python {} {} 0 {} {}".format(algorithm_file, input_file, output_file, data_file)
        
        self.log_text_edit.append("Running Steganography...")
        
        self.run_algorithm(command, "Steganography")
        
    def run_reverse_steganography(self):
        algorithm = self.algorithm_combo.currentText()
        input_file = self.output_file_edit.text()
        
        algorithm_file = algorithm + ".py"
        
        if algorithm not in ["S-UNIWARD"]:
            QMessageBox.warning(self, "Error", "Invalid algorithm selected.")
            return
        
        if not input_file.endswith(".bmp"):
            QMessageBox.warning(self, "Error", "Input file must be in BMP format.")
            return
        
        command = "python {} {} 1".format(algorithm_file, input_file)
        
        self.log_text_edit.append("Running Reverse Steganography...")
        
        self.run_algorithm(command, "Reverse Steganography")

    def run_algorithm(self, command, operation):
        start_time = time.time()
        try:
            result = os.system(command)
            execution_time = time.time() - start_time
            if result == 0:
                self.log_text_edit.append("{} completed successfully in {:.2f} seconds.".format(operation, execution_time))
            else:
                self.log_text_edit.append("{} failed.".format(operation))
        except:
            self.log_text_edit.append("Error running {}.".format(operation))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())

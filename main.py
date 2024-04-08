import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QFileDialog, QTextEdit, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtGui import QIcon
from PIL import Image, ImageChops
from hurry.filesize import size

class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stego")
        self.setMinimumSize(825, 450)

        self.algorithm_label = QLabel("Choose algorithm:", self)
        self.algorithm_label.move(25, 25)

        self.algorithm_combo = QComboBox(self)
        self.algorithm_combo.move(175, 25)
        self.algorithm_combo.addItem("S-UNIWARD")
        # self.algorithm_combo.addItem("Algorithm 2")

        self.input_file_button = QPushButton("Select Input File", self)
        self.input_file_button.move(25, 75)
        self.input_file_button.clicked.connect(self.select_input_file)

        self.input_file_label = QLabel("Input file name", self)
        self.input_file_label.setGeometry(175, 75, 200, 30)
        self.input_file_label.setWordWrap(True)

        self.output_file_label = QLabel("Output file name:", self)
        self.output_file_label.move(25, 125)

        self.output_file_edit = QLineEdit(self)
        self.output_file_edit.setGeometry(175, 125, 200, 30)
        self.output_file_edit.setPlaceholderText('Type output file name (.bmp format)')

        self.data_file_button = QPushButton("Select Data File", self)
        self.data_file_button.move(25, 175)
        self.data_file_button.clicked.connect(self.select_data_file)

        self.data_file_label = QLabel("Data file name", self)
        self.data_file_label.setGeometry(175, 175, 200, 30)
        self.data_file_label.setWordWrap(True)

        self.steganography_button = QPushButton("RUN", self)
        self.steganography_button.move(25, 225)
        self.steganography_button.clicked.connect(self.run_steganography)
        self.steganography_button.setStyleSheet("background-color: green;")

        self.reverse_steganography_button = QPushButton("RUN REVERSE", self)
        self.reverse_steganography_button.move(175, 225)
        self.reverse_steganography_button.clicked.connect(self.run_reverse_steganography)
        self.reverse_steganography_button.setStyleSheet("background-color: black;")

        self.run_analysis = QPushButton("Run analysis", self)
        self.run_analysis.move(25, 275)
        # self.run_analysis.setStyleSheet("background-color: 0f0f0f;")
        self.run_analysis.clicked.connect(self.generate_difference_image)
        
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setGeometry(25, 350, 350, 75)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setPlaceholderText("LOG WINDOW\n")

        self.label = QLabel(self)
        self.pixmap = QPixmap("stego.png")
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        self.label.setGeometry(450, 175, 300, 100)
        self.label.show()

    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input File", filter="Выберите картинку (*.bmp)")
        if file_name:

            self.input_file_label.setText(file_name)

            self.label.hide()
            self.label_picture = QLabel(self)
            self.pixmap = QPixmap(file_name)
            self.scaled_pixmap = self.pixmap.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio)
            self.label_picture.setGeometry(400+((400-self.scaled_pixmap.width())//2), 25+((400-self.scaled_pixmap.height())//2), 400, 400)
            self.label_picture.setPixmap(self.scaled_pixmap)
            self.label_picture.show()
            self.input_file_button.setStyleSheet("background-color: green;")
        
            self.size_label = QLabel("Max data size: " + str(size(self.pixmap.width()*self.pixmap.height()//320)), self)
            self.size_label.setGeometry(25, 310, 200, 30)
            self.size_label.setWordWrap(True)
            self.size_label.show()

        

    def select_data_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Data File", filter="Выберите входной файл (*.txt)")
        if file_name:
            self.data_file_label.setText(file_name)
            self.data_file_button.setStyleSheet("background-color: green;")

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
        
        self.log_text_edit.append("Running Steganography...")
        command = "python {} {} 0 {} {}".format(algorithm_file, input_file, output_file, data_file)
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
        self.log_text_edit.append("Make: output.txt")

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


    def generate_difference_image(self):

        if not self.input_file_label.text().endswith(".bmp"):
            QMessageBox.warning(self, "Error", "Input file must be in BMP format.")
            return
        
        if not self.output_file_edit.text().endswith(".bmp"):
            QMessageBox.warning(self, "Error", "Input file must be in BMP format.")
            return

        self.image1 = Image.open(self.input_file_label.text())
        self.image2 = Image.open(self.output_file_edit.text())
        self.diff = ImageChops.difference(self.image1, self.image2)
        self.mask = self.diff.convert('L').point(lambda x: 255 if x != 0 else 0, '1')
        self.masked_image = Image.composite(Image.new('RGB', self.image1.size, 'red'), self.image1, self.mask)
        self.masked_image.save('difference_image.jpg')
        self.log_text_edit.append("Analysis success! Make: difference_image.jpg")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganographyApp()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.setWindowIcon(QIcon("icon.ico"))
    window.show()
    sys.exit(app.exec_())

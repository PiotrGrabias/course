import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QComboBox


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()
        self.combo = QComboBox()

        name_label = QLabel("Distance: ")
        self.name_line_edit = QLineEdit()

        date_label = QLabel("Time (hours): ")
        self.date_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate_age)
        self.combo.addItems(['Metric (km)', 'Imperial (miles)'])
        self.output_label = QLabel("")

        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)
        grid.addWidget(self.combo, 0, 2)
        grid.addWidget(date_label, 1, 0)
        grid.addWidget(self.date_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        distance = float(self.name_line_edit.text())
        hours = float(self.date_line_edit.text())

        if self.combo.currentText() == 'Metric (km)':
            result = round(distance / hours, 2)
            self.output_label.setText(f"{result} km/h")
        if self.combo.currentText() == 'Imperial (miles)':
            result = round(distance / hours / 1.6, 2)
            self.output_label.setText(f"{result} miles/h")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())




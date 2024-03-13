import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 800)
        file_item = self.menuBar().addMenu("&File")
        help_item = self.menuBar().addMenu("&Help")
        edit_item = self.menuBar().addMenu("&Search")

        add_action = QAction(QIcon("icons/add.png"), "Add student", self)
        add_action.triggered.connect(self.insert)
        file_item.addAction(add_action)

        about_action = QAction("About", self)
        help_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        edit_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_action.triggered.connect(self.search)
        edit_item.addAction(edit_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_action)
        toolbar.addAction(edit_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_btn = QPushButton("Edit Record")
        edit_btn.clicked.connect(self.edit)

        delete_btn = QPushButton("Delete Record")
        delete_btn.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(delete_btn)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for column, data in enumerate(row_data):
                self.table.setItem(row_num, column, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        THIS APP WAS CREATED DURING THE COURSE NIBBA
        """
        self.setText(content)

class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        index = manage_window.table.currentRow()

        self.student_id = manage_window.table.item(index, 0).text()
        stud_name = manage_window.table.item(index, 1).text()
        self.student_name = QLineEdit(stud_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course_name = manage_window.table.item(index, 2).text()
        self.student_courses = QComboBox()
        courses = ["Biology", "Math"]
        self.student_courses.addItems(courses)
        self.student_courses.setCurrentText(course_name)
        layout.addWidget(self.student_courses)

        mobile_phone = manage_window.table.item(index, 3).text()
        self.mobile = QLineEdit(mobile_phone)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        submit_btn = QPushButton("Update")
        submit_btn.clicked.connect(self.update)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def update(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? Where id = ?",
                       (self.student_name.text(),
                        self.student_courses.itemText(self.student_courses.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        manage_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirmation")
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete this record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete)
        no.clicked.connect(self.close)

    def delete(self):
        index = manage_window.table.currentRow()
        student_id = manage_window.table.item(index, 0).text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id, ))
        connection.commit()
        cursor.close()
        connection.close()
        manage_window.load_data()
        self.close()
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Success")
        confirmation.setText("Record deleted successfully")
        confirmation.exec()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.search)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        items = manage_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            manage_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.student_courses = QComboBox()
        courses = ["Biology", "Math"]
        self.student_courses.addItems(courses)
        layout.addWidget(self.student_courses)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.add_student)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.student_courses.itemText(self.student_courses.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        manage_window.load_data()


app = QApplication(sys.argv)
manage_window = MainWindow()
manage_window.show()
manage_window.load_data()
sys.exit(app.exec())
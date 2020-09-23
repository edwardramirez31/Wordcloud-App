import sys
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QVBoxLayout, QApplication, QHBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtCore import pyqtSignal
import sqlite3


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()


class Login(QDialog):
    switch_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 120)
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.userWidget = QLineEdit()
        self.passwordWidget = QLineEdit()
        # Hide the password
        self.passwordWidget.setEchoMode(QLineEdit.Password)
        self.formLayout.addRow('Username:', self.userWidget)
        self.formLayout.addRow('Password:', self.passwordWidget)
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.formLayout)
        # Buttons Layout
        self.buttonsLayout = QHBoxLayout()
        self.button1 = QPushButton("OK")
        self.button1.clicked.connect(self.signal)

        self.button2 = QPushButton("Cancel")
        self.button2.clicked.connect(self.closing)
        self.buttonsLayout.addWidget(self.button1)
        self.buttonsLayout.addWidget(self.button2)
        self.mainLayout.addLayout(self.buttonsLayout)
        self.label = QLabel("")
        self.mainLayout.addWidget(self.label)

    def getDisplayText(self):
        return self.userWidget.text(), self.passwordWidget.text()

    def signal(self):
        self.switch_signal.emit()

    def closing(self):
        self.close()

    def message(self):
        self.label.setText("Username or Password Incorrect")


class Controller:

    def __init__(self):
        self.conn = sqlite3.connect('usersdb.sqlite')
        self.cur = self.conn.cursor()

    def login(self):
        self.logWidget = Login()
        self.logWidget.switch_signal.connect(self.checkEntry)
        self.logWidget.show()

    def checkEntry(self):
        user, password = self.logWidget.getDisplayText()
        self.cur.execute('''SELECT username, password FROM Users
            WHERE username=? AND password=?''', (user, password))
        if self.cur.fetchone() is None:
            self.logWidget.message()
        else:
            self.switchMainWindow()

    def switchMainWindow(self):
        self.window = MainWindow()
        self.logWidget.close()
        self.window.show()


def main():

    app = QApplication(sys.argv)
    start = Controller()
    start.login()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

import sys
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QVBoxLayout, QApplication, QHBoxLayout, QPushButton, QWidget, QLabel, QFileDialog
from PyQt5.QtCore import pyqtSignal
import sqlite3
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import time


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 500)
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.button = QPushButton("Browse Mask")
        self.button.clicked.connect(self.getFile)
        self.formLayout.addRow('Select the WordCloud contour:', self.button)
        self.imagelabel = QLabel("")
        self.formLayout.addRow("Image Selected:", self.imagelabel)
        self.button2 = QPushButton("Browse Text")
        self.button2.clicked.connect(self.getText)
        self.formLayout.addRow("Select the text:", self.button2)
        self.textSelected = QLabel("")
        self.formLayout.addRow("Text Selected:", self.textSelected)
        self.mainLayout.addLayout(self.formLayout)
        self.button3 = QPushButton("Got the Cloud")
        self.mainLayout.addWidget(self.button3)
        self.setLayout(self.mainLayout)

    def getFile(self):
        self.imagePath = QFileDialog.getOpenFileName(self, 'Open file',
                                                     'c:\\', "Image files (*.jpg *.jpeg *.png)")[0]

        self.imagelabel.setText(self.imagePath)

    def getText(self):
        self.textPath = QFileDialog.getOpenFileName(self, 'Open File', "c:\\", 'Text (*.txt)')[0]
        with open(self.textPath) as fileHandle:
            self.string = ''.join(fileHandle.readlines())
        self.textSelected.setText(self.string)


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
        self.window.button3.clicked.connect(self.getCloud)

    def getCloud(self):

        self.cloud = wordclouding(self.window.string, self.window.imagePath)


class wordclouding:
    def __init__(self, text, imagePath):
        # create the cloud object

        self.mask = np.array(Image.open(imagePath))
        time.sleep(2)
        self.wc = WordCloud(width=3000, height=2000, random_state=1, background_color='white',
                            colormap='Set2', collocations=False, stopwords=STOPWORDS, mask=self.mask)
        self.wc.generate(text)

        plt.imshow(self.wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()


def main():

    app = QApplication(sys.argv)
    start = Controller()
    start.login()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

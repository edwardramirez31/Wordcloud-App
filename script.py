import sys
from PyQt5.QtWidgets import QDialog, QLineEdit, QFormLayout, QVBoxLayout, QDialogButtonBox, QApplication


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.password_widget = QLineEdit()
        # Hide the password
        self.password_widget.setEchoMode(QLineEdit.Password)
        self.formLayout.addRow('Username:', QLineEdit())
        self.formLayout.addRow('Password:', self.password_widget)
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.formLayout)
        # Buttons Layout
        self.buttons = QDialogButtonBox()
        self.buttons.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.mainLayout.addWidget(self.buttons)


def main():
    app = QApplication(sys.argv)
    log_widget = Login()
    log_widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

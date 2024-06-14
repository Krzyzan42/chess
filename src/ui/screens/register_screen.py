from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui import *
from networking.common import *
from networking.client import *

class RegisterScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widgets()
        Client.instance.msg_recieved.connect(self._msg_recieved)

    def setup_widgets(self):
        layout = QHBoxLayout()
        left_bar = QVBoxLayout()
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.register_btn = QPushButton('Register')
        self.exit_btn = QPushButton('Exit')
        left_bar.addWidget(QLabel('Enter login'))
        left_bar.addWidget(self.login_input)
        left_bar.addWidget(QLabel('Enter password'))
        left_bar.addWidget(self.password_input)
        left_bar.addWidget(self.exit_btn)
        left_bar.addWidget(self.register_btn)
        layout.addLayout(left_bar, 25)
        layout.addStretch(75)

        self.setLayout(layout)

        self.register_btn.pressed.connect(self._register)
        self.exit_btn.pressed.connect(self._exit)

    def _register(self):
        username = self.login_input.text()
        password = self.password_input.text()
        Client.instance.send_msg(CreateAccountRequest(username, password))
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()

    def _msg_recieved(self, msg :Message):
        if msg.msg_type == MSG_CREATE_ACC_RESULT:
            self._register_response_recieved(msg)

    def _register_response_recieved(self, msg :CreateAccountResponse):
        print(msg)
        self.loading_dialog.accept()
        if msg.success:
            self._exit()

    def _exit(self):
        from ui.screens import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())


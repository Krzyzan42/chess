from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui import *
from networking.common import *
from networking.client import *
from ui.dialogs import *
import asyncio

class LoginScreen(QWidget):
    client :Client

    def __init__(self):
        super().__init__()
        self.setup_widgets()
        self.client = Client.instance

    def setup_widgets(self):
        layout = QHBoxLayout()
        left_bar = QVBoxLayout()
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.login_btn = QPushButton('Login')
        self.exit_btn = QPushButton('Exit')
        left_bar.addWidget(QLabel('Enter login'))
        left_bar.addWidget(self.login_input)
        left_bar.addWidget(QLabel('Enter password'))
        left_bar.addWidget(self.password_input)
        left_bar.addWidget(self.exit_btn)
        left_bar.addWidget(self.login_btn)
        layout.addLayout(left_bar, 25)
        layout.addStretch(75)

        self.setLayout(layout)

        self.login_btn.pressed.connect(lambda: asyncio.ensure_future(self._login()))
        self.exit_btn.pressed.connect(self._exit)

    async def _login(self):
        username = self.login_input.text()
        password = self.password_input.text()
        dialog = LoadingDialog(self)
        dialog.show()
        result = await self.client.auth.login(username, password)
        dialog.accept()

        if result.success:
            self._exit()
        else:
            dialog = ErrorDialog(self, msg=result.error_str)
            dialog.exec()
        

    def _exit(self):
        from ui.screens import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())


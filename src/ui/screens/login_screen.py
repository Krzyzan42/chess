from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui import *
from networking.common import *
from networking.client import *
from ui.dialogs import *
import asyncio

class Form(QFrame):
    pass

class Title(QLabel):
    pass

class AcceptBtn(QPushButton):
    pass

class DeclineBtn(QPushButton):
    pass

class LoginScreen(QWidget):
    client :Client

    def __init__(self):
        super().__init__()
        self.setup_widgets()
        self.client = Client.instance

    def setup_widgets(self):
        layout = QHBoxLayout()
        
        form = Form()
        central_layout = QVBoxLayout()
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_btn = AcceptBtn('Login')
        self.exit_btn = DeclineBtn('Exit')
        central_layout.addWidget(Title('Login'), alignment=Qt.AlignmentFlag.AlignHCenter)
        central_layout.addWidget(QLabel('Enter login'))
        central_layout.addWidget(self.login_input)
        central_layout.addWidget(QLabel('Enter password'))
        central_layout.addWidget(self.password_input)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.exit_btn)
        btn_layout.addWidget(self.login_btn)
        central_layout.addLayout(btn_layout)
        form.setLayout(central_layout)

        layout.addWidget(form)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.login_btn.pressed.connect(lambda: asyncio.ensure_future(self._login()))
        self.exit_btn.pressed.connect(self._exit)

    async def _login(self):
        username = self.login_input.text()
        password = self.password_input.text()
        self.dialog = LoadingDialog(self)
        self.dialog.show()
        result = await self.client.auth.login(username, password)
        self.dialog.accept()

        if result.success:
            self._exit()
        else:
            self.dialog = ErrorDialog(self, msg=result.error_str)
            self.dialog.show()
        

    def _exit(self):
        from ui.screens import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())


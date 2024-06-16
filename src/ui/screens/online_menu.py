import asyncio
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ui.menu_btn.MenuButton import MenuButton
from ui import *
from networking.client import Client

class OnlineMenu(QFrame):
    client :Client
    
    def __init__(self):
        super().__init__()
        self.setup_widgets()
        self.client = Client.instance
        self.client.auth.logged_in.connect(self._update_btn_visibility)
        self.client.auth.logged_out.connect(self._update_btn_visibility)
        self._update_btn_visibility()

    def setup_widgets(self):
        layout = QHBoxLayout()

        left_bar = QVBoxLayout()
        self.join_btn = MenuButton('Join room')
        self.create_room_btn = MenuButton('Create a room')
        self.history_btn = MenuButton('Game history')
        self.login_btn = MenuButton('Login')
        self.register_btn = MenuButton('Register')
        self.logout_btn = MenuButton('Logout')
        self.back_btn = MenuButton('Exit')

        left_bar.addWidget(self.join_btn)
        left_bar.addWidget(self.create_room_btn)
        left_bar.addWidget(self.history_btn)
        left_bar.addWidget(self.login_btn)
        left_bar.addWidget(self.register_btn)
        left_bar.addWidget(self.logout_btn)
        left_bar.addWidget(self.back_btn)
        left_bar.addStretch(1)
        left_bar.setSpacing(0)
        left_bar.setContentsMargins(0,0,0,0)
        layout.addLayout(left_bar, 3)

        background_img = QLabel()
        pixmap = QPixmap('resources/background.png')
        background_img.setPixmap(pixmap)
        background_img.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        background_img.setScaledContents(True)
        layout.addWidget(background_img, 6)

        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.setLayout(layout)

        self.join_btn.pressed.connect(self._join_pressed)
        self.create_room_btn.pressed.connect(self._create_room_pressed)
        self.back_btn.pressed.connect(self._back_pressed)
        self.login_btn.pressed.connect(self._login_pressed)
        self.register_btn.pressed.connect(self._register_pressed)
        self.logout_btn.pressed.connect(lambda: asyncio.ensure_future(self._logout_pressed()))
        self.history_btn.pressed.connect(lambda: asyncio.ensure_future(self._show_history()))

    def _update_btn_visibility(self):
        logged = self.client.auth.is_authenticated
        print(f'Is authenticated: {logged}')
        self.join_btn.setVisible(logged)
        self.create_room_btn.setVisible(logged)
        self.logout_btn.setVisible(logged)
        self.history_btn.setVisible(logged)

        self.login_btn.setVisible(not logged)
        self.register_btn.setVisible(not logged)

        self.back_btn.setVisible(True)

    def _join_pressed(self):
        from ui import RoomListScreen
        ScreenManager.instance.set_screen(RoomListScreen())
    
    def _create_room_pressed(self):
        from ui import CreateRoomScreen
        ScreenManager.instance.set_screen(CreateRoomScreen())

    def _back_pressed(self):
        from ui import MainMenu
        ScreenManager.instance.set_screen(MainMenu())

    def _login_pressed(self):
        from ui import LoginScreen
        ScreenManager.instance.set_screen(LoginScreen())

    def _register_pressed(self):
        from ui import RegisterScreen
        ScreenManager.instance.set_screen(RegisterScreen())

    async def _logout_pressed(self):
        self.dialog = LoadingDialog(self)
        self.dialog.show()
        await self.client.auth.logout()
        self.dialog.accept()

    async def _show_history(self):
        print(await self.client.game.request_history())
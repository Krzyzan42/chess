from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ui.menu_btn.MenuButton import MenuButton
from ui import *

class OnlineMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()

        left_bar = QVBoxLayout()
        join_btn = MenuButton('Join room')
        create_room_btn = MenuButton('Create a room')
        back_btn = MenuButton('Back')
        login_btn = MenuButton('Login')
        register_btn = MenuButton('Register')

        left_bar.addWidget(join_btn)
        left_bar.addWidget(create_room_btn)
        left_bar.addWidget(back_btn)
        left_bar.addWidget(login_btn)
        left_bar.addWidget(register_btn)
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

        join_btn.pressed.connect(self._join_pressed)
        create_room_btn.pressed.connect(self._create_room_pressed)
        back_btn.pressed.connect(self._back_pressed)
        login_btn.pressed.connect(self._login_pressed)
        register_btn.pressed.connect(self._register_pressed)

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
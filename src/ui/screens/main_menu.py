from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6 import QtAsyncio
from ui import *
from ui.menu_btn.MenuButton import MenuButton
from networking.client import *
from networking import settings
import asyncio

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        left_bar = QVBoxLayout()
        left_bar.setSpacing(0)
        left_bar.setContentsMargins(0,0,0,0)
        online_btn = MenuButton('Play online')
        offline_btn = MenuButton('Play offline')
        exit_btn = MenuButton('Exit')
        left_bar.addWidget(online_btn)
        left_bar.addWidget(offline_btn)
        left_bar.addWidget(exit_btn)
        left_bar.addStretch(1)
        layout.addLayout(left_bar, 3)

        background_img = QLabel()
        pixmap = QPixmap('resources/background.png')
        pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)
        background_img.setPixmap(pixmap)
        background_img.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        background_img.setScaledContents(True)
        layout.addWidget(background_img, 6)


        self.setLayout(layout)

        online_btn.pressed.connect(lambda: asyncio.ensure_future(self._online_pressed()))
        offline_btn.pressed.connect(self._offline_pressed)
        exit_btn.pressed.connect(self._exit_pressed)

    async def _online_pressed(self):
        connect_dialog = LoadingDialog(self)
        task = asyncio.create_task(Client.instance.connect_to_server(settings.server_ip, settings.server_port))
        connect_dialog.show()
        result = await task
        if result is None:
            print('connected')
            from ui import OnlineMenu
            ScreenManager.instance.set_screen(OnlineMenu())
        else:
            print(f'{result}')
        connect_dialog.accept()

    def _offline_pressed(self):
        from ui import OfflineMenu
        ScreenManager.instance.set_screen(OfflineMenu())

    def _exit_pressed(self):
        QCoreApplication.quit()
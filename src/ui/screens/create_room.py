from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui import *
import asyncio

class CreateRoomScreen(QWidget):
    client :Client

    def __init__(self):
        super().__init__()
        self.client = Client.instance
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()
        left_bar = QVBoxLayout()
        title = QLabel('Create room')
        title.setStyleSheet('font-size: 25px')
        self.room_name_input = QLineEdit()
        self.room_name_input.setPlaceholderText('Room name')
        cancel_btn = QPushButton('Cancel')
        create_btn = QPushButton('Create')
        left_bar.addWidget(title)
        left_bar.addWidget(self.room_name_input)
        left_bar.addWidget(cancel_btn)
        left_bar.addWidget(create_btn)
        layout.addLayout(left_bar, 25)
        layout.addStretch(75)

        self.setLayout(layout)

        cancel_btn.pressed.connect(self._cancel_pressed)
        create_btn.pressed.connect(lambda: asyncio.ensure_future(self._create_room()))

    def _cancel_pressed(self):
        from ui import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())
    
    async def _create_room(self):
        name = self.room_name_input.text()
        _loading_dialog = LoadingDialog()
        _loading_dialog.show()
        result = await self.client.room.create_room(name)
        _loading_dialog.accept()

        if result.success:
            self.go_to_room_screen()
        else:
            ErrorDialog(self,result.error_str).exec()

    def go_to_room_screen(self):
        from ui import RoomScreen
        ScreenManager.instance.set_screen(RoomScreen())
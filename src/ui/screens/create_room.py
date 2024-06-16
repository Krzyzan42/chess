from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui import *
import asyncio

class Form(QFrame):
    pass

class Title(QLabel):
    pass

class AcceptBtn(QPushButton):
    pass

class DeclineBtn(QPushButton):
    pass

class CreateRoomScreen(QWidget):
    client :Client

    def __init__(self):
        super().__init__()
        self.client = Client.instance
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()

        form = Form()
        central_layout = QVBoxLayout()
        title = Title('Create room')
        self.room_name_input = QLineEdit()
        self.room_name_input.setPlaceholderText('Room name')
        cancel_btn = DeclineBtn('Cancel')
        create_btn = AcceptBtn('Create')
        central_layout.addWidget(title)
        central_layout.addWidget(self.room_name_input)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(create_btn)
        central_layout.addLayout(btn_layout)
        form.setLayout(central_layout)

        layout.addWidget(form)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        cancel_btn.pressed.connect(self._cancel_pressed)
        create_btn.pressed.connect(lambda: asyncio.ensure_future(self._create_room()))

    def _cancel_pressed(self):
        from ui import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())
    
    async def _create_room(self):
        name = self.room_name_input.text()
        self._loading_dialog = LoadingDialog(ScreenManager.instance.window)
        self._loading_dialog.show()
        result = await self.client.room.create_room(name)
        self._loading_dialog.accept()
        self._loading_dialog.deleteLater()

        if result.success:
            self.go_to_room_screen()
        else:
            self.dialog = ErrorDialog(ScreenManager.instance.window,result.error_str)
            self.dialog.show()

    def go_to_room_screen(self):
        from ui import RoomScreen
        ScreenManager.instance.set_screen(RoomScreen())
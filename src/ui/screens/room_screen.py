from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui import *
from asyncio import ensure_future

class RoomScreen(QWidget):
    leave_btn :QPushButton
    host_lbl :QLabel
    guest_lbl :QLabel
    loading_dialog :LoadingDialog

    client :Client

    def __init__(self):
        super().__init__()
        self.client = Client.instance
        self.client.room.room_updated.connect(self.room_updated)
        self.client.room.left_room.connect(lambda x: ensure_future(self.leave(x)))
        self.create_widgets()
        if self.client.room:
            self.room_updated(self.client.room.current_room)

    def create_widgets(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Host: '))
        self.host_lbl = QLabel()
        layout.addWidget(self.host_lbl)
        layout.addWidget(QLabel('Guest: '))
        self.guest_lbl = QLabel()
        layout.addWidget(self.guest_lbl)
        self.leave_btn = QPushButton('Leave')
        self.leave_btn.pressed.connect(lambda: ensure_future(self._leave_pressed()))
        layout.addWidget(self.leave_btn)
        self.loading_dialog = None
        self.setLayout(layout)

    def room_updated(self, room_info :RoomInfo):
        if room_info:
            self.host_lbl.setText(f'Host: {room_info.host_name}')
            self.guest_lbl.setText(f'Guest: {room_info.guest_name}')

    async def _leave_pressed(self):
        dialog = LoadingDialog()
        dialog.show()
        await self.client.room.leave_room()
        dialog.accept()

    async def leave(self, msg :str | None):
        print(f'LEAAVVING: {msg}')
        if msg:
            ErrorDialog(ScreenManager.instance.window, msg).show()
        self.exit()

    def exit(self):
        from ui import RoomListScreen
        ScreenManager.instance.set_screen(RoomListScreen())



from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui.room_list_widget import RoomListWidget
from ui.dialogs import *
from ui import ScreenManager
from asyncio import ensure_future

class TopBar(QFrame):
    pass


class RoomListScreen(QWidget):
    client :Client

    def __init__(self):
        super().__init__()
        self._setup_widgets()

        self.client = Client.instance
        self.client.room.joined_room.connect(self._room_joined)
        ensure_future(self._refresh())

    def _setup_widgets(self):
        layout = QVBoxLayout()

        top_bar = TopBar()
        top_bar.setLayout(QHBoxLayout())
        self.back_btn = QPushButton('Back')
        self.refresh_btn = QPushButton('Refresh')
        top_bar.layout().addWidget(self.back_btn)
        top_bar.layout().addStretch(1)
        top_bar.layout().addWidget(self.refresh_btn)

        self.room_list = RoomListWidget()
        layout.addWidget(top_bar)
        layout.addWidget(self.room_list)
        self.setLayout(layout)

        self.back_btn.pressed.connect(self._go_back)
        self.refresh_btn.pressed.connect(lambda: ensure_future(self._refresh()))
        self.room_list.join.connect(lambda x: ensure_future(self._join(x)))
        self.room_list.spectate.connect(lambda x: ensure_future(self._spectate(x)))

    def _go_back(self):
        from ui.screens import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())
        
    async def _refresh(self):
        self.refresh_btn.setEnabled(False)
        self.room_list.set_loading()
        result :list[RoomInfo] = await self.client.room.list_rooms()
        self.room_list.set_rooms(result)
        self.refresh_btn.setEnabled(True)

    async def _join(self, room :RoomInfo):
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()
        result = await self.client.room.join_room(room.room_id, False)
        self.loading_dialog.accept()

        if not result.success:
            ErrorDialog(None, result.error_str).show()

    async def _spectate(self, room :RoomInfo):
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()
        result = await self.client.room.join_room(room.room_id, True)
        self.loading_dialog.accept()

        if not result.success:
            ErrorDialog(None, result.error_str).show()

    def _room_joined(self, room_info):
        from ui.screens.room_screen import RoomScreen
        ScreenManager.instance.set_screen(RoomScreen())
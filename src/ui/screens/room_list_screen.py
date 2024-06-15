from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui.room_list_widget import RoomListWidget
from ui.dialogs import *
from ui import ScreenManager
from asyncio import ensure_future

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
        self.back_btn = QPushButton('Back')
        self.refresh_btn = QPushButton('Refresh')
        self.join_btn = QPushButton('Join')
        self.spectate_btn = QPushButton('Spectate')
        self.room_list = RoomListWidget()
        
        layout.addWidget(self.back_btn)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.join_btn)
        layout.addWidget(self.spectate_btn)
        layout.addWidget(self.room_list)
        self.setLayout(layout)

        self.back_btn.pressed.connect(self._go_back)
        self.refresh_btn.pressed.connect(lambda: ensure_future(self._refresh()))
        self.join_btn.pressed.connect(lambda: ensure_future(self._join(False)))
        self.spectate_btn.pressed.connect(lambda: ensure_future(self._join(True)))
        self.room_list.selection_changed.connect(self._on_room_selected)
        self._on_room_selected(None)

    def _on_room_selected(self, room :RoomInfo | None):
        print(f'Selected room: {room}')
        is_selected = room is not None
        self.join_btn.setEnabled(is_selected)

    def _go_back(self):
        from ui.screens import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())
        
    async def _refresh(self):
        self.refresh_btn.setEnabled(False)
        self.room_list.set_loading()
        result :list[RoomInfo] = await self.client.room.list_rooms()
        self.room_list.set_rooms(result)
        self.refresh_btn.setEnabled(True)

    async def _join(self, spectate):
        room = self.room_list.get_current_room()
        if room is None:
            return

        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()
        result = await self.client.room.join_room(room.room_id, spectate)
        self.loading_dialog.accept()

        if not result.success:
            ErrorDialog(self, result.error_str).exec()

    def _room_joined(self, room_info):
        from ui.screens.room_screen import RoomScreen
        ScreenManager.instance.set_screen(RoomScreen())
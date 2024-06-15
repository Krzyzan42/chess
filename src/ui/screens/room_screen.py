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
        self.client.room.left_room.connect(self.exit)
        self.client.game.game_started.connect(self._go_to_game)
        self.create_widgets()

        if self.client.room:
            self.room_updated(self.client.room.current_room)

    def create_widgets(self):
        layout = QVBoxLayout()
        self.host_lbl = QLabel()
        self.guest_lbl = QLabel()
        self.leave_btn = QPushButton('Leave')
        self.start_btn = QPushButton('Start')
        layout.addWidget(QLabel('Host: '))
        layout.addWidget(self.host_lbl)
        layout.addWidget(QLabel('Guest: '))
        layout.addWidget(self.guest_lbl)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.leave_btn)
        self.loading_dialog = None
        self.setLayout(layout)

        self.leave_btn.pressed.connect(lambda: ensure_future(self._leave_pressed()))
        self.start_btn.pressed.connect(lambda: ensure_future(self._start_pressed()))

    def room_updated(self, room_info :RoomInfo):
        if room_info:
            self.host_lbl.setText(f'Host: {room_info.host_name}')
            self.guest_lbl.setText(f'Guest: {room_info.guest_name}')
            self.start_btn.setVisible(not self.client.room.is_spectating)

    async def _leave_pressed(self):
        dialog = LoadingDialog()
        dialog.show()
        await self.client.room.leave_room()
        dialog.accept()

    async def _start_pressed(self):
        await self.client.room.start_game()

    def _go_to_game(self, game :GameState):
        from ui.screens.chess_vs_online import ChessVsOnline
        from ui.screens.chess_spectate import ChessSpectate
        if game.is_spectating:
            ScreenManager.instance.set_screen(ChessSpectate())
        else:
            ScreenManager.instance.set_screen(ChessVsOnline())

    def leave(self, msg :str | None):
        if msg:
            dialog = ErrorDialog(ScreenManager.instance.window, msg)
            dialog.show()
            dialog.accepted.connect(self.exit)
        else:
            self.exit()

    def exit(self):
        from ui import RoomListScreen
        ScreenManager.instance.set_screen(RoomListScreen())



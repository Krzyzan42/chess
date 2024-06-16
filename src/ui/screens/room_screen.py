from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from networking.common import *
from networking.client import *
from ui import *
from asyncio import ensure_future

from ui.chess_game.end_dialog import EndDialog

class Title(QLabel):
    pass
class ImgLbl(QLabel):
    pass
class PlayerLabel(QLabel):
    pass
class VsLabel(QLabel):
    pass
class TopBar(QFrame):
    pass
class Content(QFrame):
    pass
class AcceptBtn(QPushButton):
    pass

class RoomScreen(QFrame):
    leave_btn :QPushButton
    title_lbl :QLabel
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
        top_bar = TopBar()
        top_bar.setLayout(QVBoxLayout())
        self.title_lbl = Title('Room')
        top_bar.layout().addWidget(self.title_lbl, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(top_bar)

        content = Content()
        vs_layout = QHBoxLayout()
        white_layout = QVBoxLayout()
        white_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        white_img = ImgLbl()
        white_img.setScaledContents(True)
        white_img.setPixmap(QPixmap('resources/white_pawn.png'))
        self.host_lbl = PlayerLabel('White')
        self.host_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        white_layout.addWidget(white_img)
        white_layout.addWidget(self.host_lbl)

        vs_lbl = VsLabel('VS')
        vs_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        black_layout = QVBoxLayout()
        black_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        black_img = ImgLbl()
        black_img.setScaledContents(True)
        black_img.setPixmap(QPixmap('resources/black_pawn.png'))
        self.guest_lbl = PlayerLabel('Black')
        self.guest_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        black_layout.addWidget(black_img)
        black_layout.addWidget(self.guest_lbl)
        vs_layout.addLayout(white_layout)
        vs_layout.addWidget(vs_lbl)
        vs_layout.addLayout(black_layout)
        vs_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content.setLayout(vs_layout)

        btn_layout = QHBoxLayout()
        self.leave_btn = QPushButton('Leave')
        self.start_btn = AcceptBtn('Start')
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.leave_btn)
        btn_layout.addWidget(self.start_btn)

        layout.addWidget(content)
        layout.addLayout(btn_layout)
        self.loading_dialog = None
        self.setLayout(layout)

        self.leave_btn.pressed.connect(lambda: ensure_future(self._leave_pressed()))
        self.start_btn.pressed.connect(lambda: ensure_future(self._start_pressed()))
        
        layout.setContentsMargins(0,0,0,0)

    def room_updated(self, room_info :RoomInfo):
        if room_info:
            self.title_lbl.setText(f'{room_info.room_name}')
            self.host_lbl.setText(f'{room_info.host_name}')
            guest_txt = room_info.guest_name
            if not guest_txt:
                guest_txt = 'Waiting to join'
            self.guest_lbl.setText(f'{guest_txt}')
            self.start_btn.setVisible(room_info.host_name == self.client.auth.current_user)
            self.start_btn.setEnabled(room_info.guest_name is not None)

    async def _leave_pressed(self):
        self.dialog = LoadingDialog(ScreenManager.instance.window)
        self.dialog.show()
        await self.client.room.leave_room()
        self.dialog.accept()

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



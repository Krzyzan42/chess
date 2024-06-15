from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui.screen_manager import ScreenManager
from ui.chess_game import ChessGame, EndDialog
from ui.menu_btn.MenuButton import MenuButton
from networking.common import *
from networking.client import Client
import chess
from asyncio import ensure_future

class ChessSpectate(QWidget):
    _chess_game :ChessGame
    _client :Client

    def __init__(self):
        super().__init__()
        self.setup_widgets()

        self._client = Client.instance
        self._client.game.game_updated.connect(self._update_game)
        self._client.game.game_finished.connect(self._game_finished)
        self._client.game.left_spectate.connect(self._go_back)
        self._update_game(self._client.game.game)
    
    def setup_widgets(self):
        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.leave_btn = MenuButton('Leave')
        top_bar.addWidget(self.leave_btn)
        top_bar.addStretch(1)
        self._chess_game = ChessGame()

        layout.addLayout(top_bar)
        layout.addWidget(self._chess_game)

        self.setLayout(layout)

        self.leave_btn.pressed.connect(lambda: ensure_future(self.surrender_clicked()))

    async def surrender_clicked(self):
        self.leave_btn.setEnabled(False)
        await self._client.game.leave()

    def _update_game(self, game :GameState):
        if game is None:
            self._chess_game.set_board(None)
            self._chess_game.set_messages(None)
            self._chess_game.set_move_history([])
        else:
            self._chess_game.set_board(game.board)
            self._chess_game.set_selectable(game.can_move)
            self._chess_game.set_messages(game.messages)
            self._chess_game.set_move_history(game.moves)

    def _game_finished(self, win :bool | None, reason :str):
        dialog = EndDialog()
        dialog.set_win(win, reason)
        dialog.accepted.connect(self._go_back)
        dialog.show()
        self.dialog = dialog

    def _go_back(self):
        from ui.screens.room_list_screen import RoomListScreen
        ScreenManager.instance.set_screen(RoomListScreen())
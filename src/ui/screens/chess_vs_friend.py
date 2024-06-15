from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui.screen_manager import ScreenManager
from ui.chess_game import ChessGame
import chess

class ChessVsFriend(QWidget):
    game :chess.Board
    ui_game :ChessGame

    _msgs :list[str]
    _move_history :list[str]

    def __init__(self):
        super().__init__()
        self.setup_widgets()
        self.setup_game()
        
    def setup_widgets(self):
        layout = QVBoxLayout()
        self.ui_game = ChessGame()
        layout.addWidget(self.ui_game)
        self.setLayout(layout)

    def setup_game(self):
        self.game = chess.Board()
        self.ui_game.set_board(self.game)
        self.ui_game.move_selected.connect(self.make_move)
        self.ui_game.msg_sent.connect(self.record_message)
        self._msgs = []
        self._move_history = []

    def make_move(self, move :chess.Move):
        self.game.push(move)
        self.ui_game.set_board(self.game)
        self._move_history.append(move.uci())
        self.ui_game.set_move_history(self._move_history)

    def record_message(self, msg :str):
        self._msgs.append(msg)
        self.ui_game.set_messages(self._msgs)
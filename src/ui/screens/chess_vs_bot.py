from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui.chess_game.end_dialog import EndDialog
from ui.screen_manager import ScreenManager
from ui.chess_game import ChessGame
import chess
from stockfish import Stockfish

class TopBar(QFrame):
    exit = Signal()

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        btn = QPushButton('Exit')
        btn.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )
        btn.pressed.connect(self.exit)
        layout.addWidget(btn)
        layout.addStretch(1)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

class ChessVsBot(QWidget):
    game :chess.Board
    ui_game :ChessGame

    _msgs :list[str]
    _move_history :list[str]
    _stockfish :Stockfish
    _calc_ai_move = Signal()

    def __init__(self):
        super().__init__()
        self.setup_widgets()
        self.setup_game()
        
    def setup_widgets(self):
        layout = QVBoxLayout()
        self.ui_game = ChessGame()
        self.ui_game.set_messages_visible(False)
        top_bar = TopBar()
        top_bar.exit.connect(self.exit)
        layout.addWidget(top_bar)
        layout.addWidget(self.ui_game)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def setup_game(self):
        self.game = chess.Board()
        self.ui_game.set_board(self.game)
        self.ui_game.move_selected.connect(self.make_move)
        self.ui_game.msg_sent.connect(self.record_message)
        self._msgs = []
        self._move_history = []
        self._stockfish = Stockfish()
        self._stockfish.update_engine_parameters({'UCI_Chess960': True})
        self._calc_ai_move.connect(self.move_bot)

    def make_move(self, move :chess.Move):
        self.game.push(move)
        self.ui_game.set_board(self.game)
        self._move_history.append(move.uci())
        self.ui_game.set_move_history(self._move_history)
        if self.game.is_game_over():
            print('its jover')
            self.finish_game(self.game.outcome())
            return
        fen = chess.square_name(move.from_square) + chess.square_name(move.to_square)
        self._stockfish.make_moves_from_current_position([fen])

        self.ui_game.set_selectable(not self.ui_game.is_selectable())
        selectable = self.ui_game.is_selectable()
        if not selectable:
            self._calc_ai_move.emit()

    def move_bot(self):
        move = self._stockfish.get_best_move_time(1000)
        from_sqr = chess.parse_square(move[:2])
        to_sqr = chess.parse_square(move[2:])

        self.make_move(chess.Move(from_sqr, to_sqr))

    def record_message(self, msg :str):
        self._msgs.append(msg)
        self.ui_game.set_messages(self._msgs)

    def finish_game(self, outcome :chess.Outcome):
        win = outcome.winner
        reason = outcome.termination.name
        reason = reason.capitalize()
        reason = reason.replace('_', ' ')
        dialog = EndDialog(self)
        dialog.set_win(win, reason)
        dialog.accepted.connect(self.exit)
        dialog.show()
        self.dialog = dialog

    def exit(self):
        from ui.screens import OfflineMenu
        ScreenManager.instance.set_screen(OfflineMenu())
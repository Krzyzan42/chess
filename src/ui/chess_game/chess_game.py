from PySide6.QtCore import *
from PySide6.QtWidgets import *
from .chess_widget import Board
from .message_bar import MessageBar
from .history_bar import HistoryBar
from .info_widget import InfoWidget
import chess

class ChessGame(QWidget):
    move_selected = Signal(chess.Move)
    msg_sent = Signal(str)

    _chessboard :Board
    _msg_bar :MessageBar

    def __init__(self):
        super().__init__()
        self._setup_widgets()

    def set_board(self, board :chess.Board):
        self._chessboard.set_board(board)

    def set_messages(self, msgs: list[str] | None):
        self._msg_bar.set_messages(msgs)

    def set_move_history(self, moves: list[chess.Move]):
        self._history_bar.set_history(moves)

    def show_victory_screen(self, who_won :chess.Color, reason :bool):
        self.set_selectable(False)

    def set_selectable(self, selectable :bool):
        self._chessboard.set_selectable(selectable)

    def show_messages(self, show :bool):
        pass

    def set_names(self, black_name :str, white_name :str):
        pass

    def _setup_widgets(self):
        layout = QHBoxLayout()


        self._chessboard = Board()

        left_widget = QWidget()
        left_bar = QVBoxLayout()
        self._info_widget = InfoWidget()

        self._tab_widget = QTabWidget()
        self._msg_bar = MessageBar()
        self._history_bar = HistoryBar()
        self._tab_widget.addTab(self._msg_bar, 'Chatroom')
        self._tab_widget.addTab(self._history_bar, 'Moves')
        self._tab_widget.tabBar().setExpanding(True)
        left_bar.addWidget(self._info_widget)
        left_bar.addWidget(self._tab_widget)
        left_widget.setLayout(left_bar)
        left_widget.setMaximumHeight(self._chessboard.height())

        layout.addWidget(self._chessboard)
        layout.addWidget(left_widget)
        self.setLayout(layout)

        self._chessboard.move_selected.connect(self.move_selected)
        self._msg_bar.msg_sent.connect(self.msg_sent)
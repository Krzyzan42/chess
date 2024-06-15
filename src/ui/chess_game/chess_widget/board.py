from PySide6.QtCore import *
from PySide6.QtWidgets import *
from . import *
import chess

class Board(QWidget):
    move_selected = Signal(chess.Move)

    def __init__(self):
        super().__init__()
        self.setup_game_context()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QVBoxLayout()
        self.board_painter = BoardPainter()
        layout.addWidget(BoardPainter())
        self.setLayout(layout)

    def set_board(self, board :chess.Board):
        Context.board = board
        Context.selection.clear_selection()
        # self.repaint()

    def set_selectable(self, selectable :bool):
        Context.selection.set_selectable(selectable)

    def setup_game_context(self):
        Context.params = BoardParams()
        Context.pixmaps = get_figure_pixmaps()
        Context.selection = BoardSelection()
        Context.selection.set_selectable(True)
        Context.selection.selection_changed.connect(self.repaint)
        Context.selection.move_selected.connect(self.move_selected)
        Context.board = None

from PySide6.QtCore import *
from . import Context
import chess

class BoardSelection(QObject):
    square :chess.Square | None
    selection_changed = Signal()
    move_selected = Signal(chess.Move)

    _is_selectable :bool

    def __init__(self):
        super().__init__()
        self.square = None
        self._is_selectable = False
        self.selection_changed.connect(lambda: print(self.square))
        self.move_selected.connect(lambda x: print(x))

    def possible_moves(self) -> list[chess.Square] | None:
        if Context.board is None or self.square is None:
            return None
        else:
            return self._moves_from_square(self.square, Context.board)

    def select(self, square):
        if not self._is_selectable or Context.board is None:
            return

        if self.square == None:
            moves = self._moves_from_square(square, Context.board)
            if len(moves) > 0:
                self.square = square
                self.selection_changed.emit()
        elif self.square == square:
            self.square = None
            self.selection_changed.emit()
        else:
            moves = self._moves_from_square(self.square, Context.board)
            if square in moves:
                selected_move = chess.Move(self.square, square)
                self.square = None
                self.selection_changed.emit()
                self.move_selected.emit(selected_move)

    def set_selectable(self, selectable):
        self._is_selectable = selectable
        if self.square and not selectable:
            self.square = None
            self.selection_changed.emit()
        
    def clear_selection(self):
        self.square = None
        self.selection_changed.emit()

    def _moves_from_square(self, square :chess.Square, board :chess.Board):
        possible_moves = board.generate_legal_moves(1 << square)
        possible_moves = [move.to_square for move in possible_moves]
        return possible_moves
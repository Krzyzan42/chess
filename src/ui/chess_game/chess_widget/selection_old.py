from chess import Square, square_name
from PySide6.QtCore import QObject, Signal

class BoardSelection(QObject):
    selection_changed = Signal(Square)
    _square :Square

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._square = None

    @property
    def selected_square(self) -> Square | None:
        return self._square

    # Convinence function for drawing
    def possible_moves(self) -> list[Square] | None:
        if self._square is None:
            print('Trying to get possible moves of unselectable square')
            return None
        else:
            moves = Context.controller.possible_moves(self._square)
            return [move.to_square for move in moves]

    def is_selectable(self, square) -> bool:
        moves = Context.controller.possible_moves(square)
        return len(list(moves)) > 0
    
    def select(self, square):
        if not self.is_selectable(square):
            print('trying to select unselectable square')
            return

        if square != self._square:
            self._square = square
            self.selection_changed.emit(square)

    def deselect(self):
        self._square = None
        self.selection_changed.emit(None)

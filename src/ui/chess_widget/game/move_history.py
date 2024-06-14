from PySide6.QtCore import QObject, Signal
from chess import Move

class MoveHistory(QObject):
    moved = Signal(Move)

    def __init__(self) -> None:
        self._history :list[Move] = []
        super().__init__()

    def add_move(self, move :Move):
        self._history.append(move)
        self.moved.emit(move)

    def get_history(self) -> list[Move]:
        return list(self._history)
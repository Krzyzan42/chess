from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from chess import Square

class BoardParams:
    light_color :QColor
    dark_color :QColor
    board_size :QSize
    inverted :bool

    def __init__(self) -> None:
        self.light_color = QColor(238, 238, 210)
        self.dark_color = QColor(118, 150, 86)
        self.board_size = QSize(480, 480)

    @property
    def square_size(self):
        return self.board_size / 8
    
    def xy_to_square(self, x :int, y :int) -> Square:
        return x + y * 8

    def square_to_xy(self, square :Square) -> tuple[int, int]:
        return (square & 7, square >> 3)
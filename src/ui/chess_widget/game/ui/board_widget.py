from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QColor
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Slot
from chess import Square, SQUARES
from chess_widget.game import Context
from .square_widget import BoardSquare

class BoardPainter(QWidget):
    square_clicked = Signal(Square)

    def __init__(   self, 
                    *args, 
                    **kwargs
                ):
        super().__init__(*args, **kwargs)
        self.setFixedSize(Context.params.board_size)
        self.setMinimumSize(Context.params.board_size)
        self.setup_squares()

        Context.selection.selection_changed.connect(lambda x: self.repaint())
        Context.controller.board_changed.connect(lambda x: self.repaint())

        self.setGeometry(0, 0, 480, 480)

    def setup_squares(self):
        self.setLayout(None)
        for square in SQUARES:
            self.create_ui_square(square)
                
    def create_ui_square(self, square :Square):
        sqr_width = Context.params.board_size.width() / 8
        sqr_height = Context.params.board_size.height() / 8
        x, y = self.square_to_xy(square)
        is_white = (x + y) % 2 == 0
        sqr_x = sqr_width * x
        sqr_y = sqr_height * y

        board_square = BoardSquare(square, is_white)
        board_square.setGeometry(sqr_x, sqr_y, sqr_width, sqr_height)
        board_square.setParent(self)
        board_square.square_clicked.connect(self.square_clicked)

    def square_to_xy(self, square :Square) -> tuple[int, int]:
        return (square & 7, square >> 3)

    @Slot()
    def update(self):
        self.repaint()


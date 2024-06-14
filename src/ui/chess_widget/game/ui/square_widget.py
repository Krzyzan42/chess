from chess_widget.game import Context
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QMouseEvent, QPaintEvent, QPainter, QColor
from chess import Square, Piece, KING
from enum import Enum, auto

class BoardSquare(QWidget):
    square_clicked = Signal(Square)

    # Actual chess board square
    square :Square

    # Some drawing parameters
    light_color :QColor
    dark_color :QColor
    threathend_color :QColor
    is_white :bool
    
    def __init__(self, square :Square, is_white :bool) -> None:
        super().__init__()
        self.light_color = Context.params.light_color
        self.dark_color = Context.params.dark_color
        self.threathend_color = QColor(180, 60, 60)
        self.check_color = QColor(200, 30, 30)
        self.is_white = is_white

        self.square = square

    def paintEvent(self, _: QPaintEvent) -> None:
        bg_type = self.get_background_type()
        default_color = self.light_color if self.is_white else self.dark_color
        color = None
        draw_dot = False
        if bg_type == Background.Normal:
            color = default_color
        elif bg_type == Background.Selected:
            color = default_color
            color = QColor.darker(color)
        elif bg_type == Background.Threathened:
            color = self.threathend_color
        elif bg_type == Background.Moveable:
            color = default_color
            draw_dot = True
        elif bg_type == Background.Check:
            color = self.check_color

        painter = QPainter(self)
        painter.setBrush(color)
        painter.setPen(color)
        painter.drawRect(0, 0, self.size().width(), self.size().height())

        if draw_dot:
            col = QColor(100, 100, 100)
            rad = 10
            painter.setBrush(col)
            painter.setPen(col)
            x = self.size().width() / 2 - rad / 2
            y = self.size().height() / 2 - rad / 2
            painter.drawEllipse(x, y, rad, rad)

        board = Context.controller.get_board()
        if board.piece_at(self.square) != None:
            self.draw_piece(board.piece_at(self.square))

    def get_background_type(self) -> 'Background':
        board = Context.controller.get_board()
        piece = board.piece_at(self.square)
        if piece and piece.piece_type == KING and piece.color == board.turn:
            if board.is_check() or board.is_checkmate():
                return Background.Check

        if Context.selection.selected_square is not None:
            if self.square == Context.selection.selected_square:
                return Background.Selected
            piece = board.piece_at(self.square)
            if piece is not None and self.square in Context.selection.possible_moves():
                if piece.piece_type == KING:
                    return Background.Check
                else:
                    return Background.Threathened
            if self.square in Context.selection.possible_moves():
                return Background.Moveable

        return Background.Normal
        

    def draw_piece(self, piece :Piece):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QColor(255, 255, 255))
        pixmap = Context.pixmaps[(piece.piece_type, piece.color)]
        painter.drawPixmap(0, 0, pixmap)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.square_clicked.emit(self.square)
        event.accept()
    
class Background(Enum):
    Normal = auto()
    Moveable = auto()
    Selected = auto()
    Threathened = auto()
    Check = auto()
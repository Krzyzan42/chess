from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap
from chess import (
    QUEEN,
    KNIGHT,
    BISHOP,
    ROOK, 
    PieceType
)

class PromotionSelect(QWidget):
    piece_selected = Signal(PieceType)

    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.setup_buttons()
        self.hide()

    def setup_buttons(self):
        figures = [QUEEN, KNIGHT, BISHOP, ROOK]
        names = ['QUEEN', 'KNIGHT', 'BISHOP', 'ROOK']
        for fig, name in zip(figures, names):
            self.add_btn(name, fig)

    def add_btn(self, text, piece_type):
        btn = QPushButton()
        btn.setText(text)
        btn.pressed.connect(lambda: self.piece_selected.emit(piece_type))
        btn.pressed.connect(self.hide)
        self.layout().addWidget(btn)

    def show_to_select(self):
        self.show()
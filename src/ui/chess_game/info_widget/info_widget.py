from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class ImgLbl(QLabel):
    pass

class PlayerLabel(QLabel):
    pass

class VsLabel(QLabel):
    pass

class InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()

        white_layout = QVBoxLayout()
        white_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        white_img = ImgLbl()
        white_img.setPixmap(QPixmap('resources/white_pawn.png'))
        white_lbl = PlayerLabel('White')
        white_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        white_layout.addWidget(white_img)
        white_layout.addWidget(white_lbl)

        vs_lbl = VsLabel('VS')
        vs_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        black_layout = QVBoxLayout()
        black_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        black_img = ImgLbl()
        black_img.setPixmap(QPixmap('resources/black_pawn.png'))
        black_lbl = PlayerLabel('Black')
        black_lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        black_layout.addWidget(black_img)
        black_layout.addWidget(black_lbl)

        layout.addLayout(white_layout)
        layout.addWidget(vs_lbl)
        layout.addLayout(black_layout)
        self.setLayout(layout)


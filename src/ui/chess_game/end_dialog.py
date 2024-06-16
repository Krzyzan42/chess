from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui.chess_game.info_widget import InfoWidget
import chess

class Title(QLabel):
    pass
class Reason(QLabel):
    pass

class EndDialog(QDialog):
    _result_lbl :QLabel
    _reason_lbl :QLabel

    def __init__(self, parent :QWidget | None):
        super().__init__(parent)

        self.setModal(True)
        self.setGeometry(self.x(), self.y(), 450, 300)

        layout = QVBoxLayout()
        self._result_lbl = Title('Unknown won')
        self._result_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._result_lbl.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self._reason_lbl = Reason('Unknown reason')
        self._reason_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._reason_lbl.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        info_widget = InfoWidget()
        close_btn = QPushButton('Ok')
        layout.addWidget(self._result_lbl)
        layout.addWidget(self._reason_lbl)
        layout.addWidget(info_widget)
        layout.addWidget(close_btn)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        close_btn.pressed.connect(self.accept)

    def set_win(self, win :chess.Color | None, reason :str | None):
        if win == None:
            self._result_lbl.setText('DRAW')
        elif win == chess.WHITE:
            self._result_lbl.setText('WHITE WON')
        else:
            self._result_lbl.setText('BLACK WON')

        if reason:
            self._reason_lbl.setText(f'{reason}')
        else:
            self._reason_lbl.setText('Unknown reason')

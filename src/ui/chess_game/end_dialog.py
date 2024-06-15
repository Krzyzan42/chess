from PySide6.QtCore import *
from PySide6.QtWidgets import *
import chess

class EndDialog(QDialog):
    _result_lbl :QLabel
    _reason_lbl :QLabel


    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setModal(True)

        layout = QVBoxLayout()
        self._result_lbl = QLabel('Unknown won')
        self._reason_lbl = QLabel('Unknown reason')
        close_btn = QPushButton('Ok')
        layout.addWidget(self._result_lbl)
        layout.addWidget(self._reason_lbl)
        layout.addWidget(close_btn)
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
            self._reason_lbl.setText(f'By {reason}')
        else:
            self._reason_lbl.setText('Unknown reason')

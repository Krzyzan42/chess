from PySide6.QtCore import *
from PySide6.QtWidgets import *

class TitleLbl(QLabel):
    pass

class MsgLbl(QLabel):
    pass

class LoadingDialog(QDialog):
    _title_lbl :TitleLbl
    _message_lbl :MsgLbl

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)

        layout = QVBoxLayout()
        self._title_lbl = TitleLbl('Wait')
        self._title_lbl.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        layout.addWidget(self._title_lbl)
        layout.setContentsMargins(0,0,0,0)

        self._message_lbl = MsgLbl('Loading...')
        layout.addWidget(self._message_lbl, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)
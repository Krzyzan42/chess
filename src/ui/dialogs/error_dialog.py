from PySide6.QtCore import *
from PySide6.QtWidgets import *

class TitleLbl(QLabel):
    pass

class MsgLbl(QLabel):
    pass

class ErrorDialog(QDialog):
    _title_lbl :QLabel
    _message_lbl :MsgLbl

    def __init__(self, parent=None, msg :str = 'Message', title :str = 'Error'):
        super().__init__(parent)
        self.setModal(True)

        layout = QVBoxLayout()
        self._title_lbl = TitleLbl()
        self._title_lbl.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        layout.addWidget(self._title_lbl)
        layout.setContentsMargins(0,0,0,0)

        self._message_lbl = MsgLbl()
        self.btn = QPushButton('Close')
        self.btn.pressed.connect(self.accept)
        layout.addWidget(self._message_lbl, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

        self.set_msg(msg)
        self.set_title(title)

    def set_msg(self, msg :str):
        self._message_lbl.setText(msg)

    def set_title(self, title :str):
        self._title_lbl.setText(title)
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class ErrorDialog(QDialog):
    def __init__(self, parent=None, msg :str = ''):
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setModal(True)

        layout = QVBoxLayout()
        self.label = QLabel(msg)
        self.btn = QPushButton('Close')
        self.btn.pressed.connect(self.accept)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def set_msg(self, msg :str = ''):
        self.label.setText(msg)
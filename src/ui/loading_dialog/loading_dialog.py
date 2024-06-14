from PySide6.QtCore import *
from PySide6.QtWidgets import *

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setModal(True)

        layout = QVBoxLayout()
        self.label = QLabel('Loading, please wait...')
        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_message(self, text):
        pass
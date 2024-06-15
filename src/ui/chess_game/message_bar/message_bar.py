from PySide6.QtCore import *
from PySide6.QtWidgets import *

class MessageBar(QWidget):
    msg_sent = Signal(str)

    _msg_bar :QVBoxLayout
    _msg_input :QLineEdit
    _send_btn :QPushButton

    def __init__(self):
        super().__init__()
        self._setup_widgets()

    def set_messages(self, msgs :list[str] | None):
        while self._msg_bar.count():
            item = self._msg_bar.takeAt(0) 
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if msgs:
            for msg in msgs:
                self._msg_bar.addWidget(QLabel(msg))
        self._msg_bar.addStretch(1)

    def _setup_widgets(self):
        layout = QVBoxLayout()

        self._msg_bar = QVBoxLayout()
        self._msg_bar.addStretch(1)
        
        input_layout = QHBoxLayout()
        self._msg_input = QLineEdit()
        self._send_btn = QPushButton('Send')
        self._send_btn.setEnabled(False)
        input_layout.addWidget(self._msg_input)
        input_layout.addWidget(self._send_btn)

        layout.addLayout(self._msg_bar, 1)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        self._send_btn.pressed.connect(self._send_pressed)
        self._msg_input.textChanged.connect(self._text_changed)

    def _text_changed(self, text :str):
        self._send_btn.setEnabled(text != '')

    def _send_pressed(self):
        txt = self._msg_input.text()
        self._msg_input.clear()
        self.msg_sent.emit(txt)
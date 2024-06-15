from PySide6.QtCore import *
from PySide6.QtWidgets import *

class HistoryBar(QWidget):
    _history_bar :QVBoxLayout

    def __init__(self):
        super().__init__()
        self._setup_widgets()

    def set_history(self, msgs :list[str] | None):
        while self._history_bar.count():
            item = self._history_bar.takeAt(0) 
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if msgs:
            for msg in msgs:
                self._history_bar.addWidget(QLabel(msg))
        self._history_bar.addStretch(1)

    def _setup_widgets(self):
        self._history_bar = QVBoxLayout()
        self._history_bar.addStretch(1)
        
        self.setLayout(self._history_bar)
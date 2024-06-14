from PySide6.QtCore import *
from PySide6.QtWidgets import *
from ui import *

class OfflineMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()
        left_bar = QVBoxLayout()
        friend_btn = QPushButton('Play vs friend')
        bot_btn = QPushButton('Play vs bot')
        back_btn = QPushButton('Back')
        left_bar.addWidget(friend_btn)
        left_bar.addWidget(bot_btn)
        left_bar.addWidget(back_btn)
        layout.addLayout(left_bar, 25)
        layout.addStretch(75)

        self.setLayout(layout)

        friend_btn.pressed.connect(self._friend_pressed)
        bot_btn.pressed.connect(self._bot_pressed)
        back_btn.pressed.connect(self._back_pressed)

    def _friend_pressed(self):
        raise NotImplementedError('No friends. Womp womp')
    
    def _bot_pressed(self):
        raise NotImplementedError('Just assume you lost')

    def _back_pressed(self):
        from ui import MainMenu
        ScreenManager.instance.set_screen(MainMenu())
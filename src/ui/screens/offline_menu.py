from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ui import *

class MenuButton(QPushButton):
    pass

class OfflineMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()
        left_bar = QVBoxLayout()
        friend_btn = MenuButton('Play vs friend')
        bot_btn = MenuButton('Play vs bot')
        back_btn = MenuButton('Back')
        left_bar.addWidget(friend_btn)
        left_bar.addWidget(bot_btn)
        left_bar.addWidget(back_btn)
        left_bar.addStretch(1)
        layout.addLayout(left_bar, 3)
        
        background_img = QLabel()
        pixmap = QPixmap('resources/background.png')
        pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)
        background_img.setPixmap(pixmap)
        background_img.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        background_img.setScaledContents(True)
        layout.addWidget(background_img, 6)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        friend_btn.pressed.connect(self._friend_pressed)
        bot_btn.pressed.connect(self._bot_pressed)
        back_btn.pressed.connect(self._back_pressed)

    def _friend_pressed(self):
        from ui.screens.chess_vs_friend import ChessVsFriend
        ScreenManager.instance.set_screen(ChessVsFriend())
    
    def _bot_pressed(self):
        from ui.screens.chess_vs_bot import ChessVsBot
        ScreenManager.instance.set_screen(ChessVsBot())

    def _back_pressed(self):
        from ui import MainMenu
        ScreenManager.instance.set_screen(MainMenu())
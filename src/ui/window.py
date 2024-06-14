from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui.screen_manager import ScreenManager

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(900, 600)
        self.setStyleSheet(self.get_style())

        scr_mng = ScreenManager.instance

        scr_mng.screen_changed.connect(self.change_screen)
        self.setCentralWidget(scr_mng.current_screen)

    def get_style(self) -> str:
        with open('resources/style.css') as file:
            return file.read()

    @Slot(QWidget)
    def change_screen(self, widget :QWidget):
        self.setCentralWidget(widget)


from PySide6.QtCore import *
from PySide6.QtWidgets import *

class ScreenManager(QObject):
    screen_changed = Signal(QWidget)
    current_screen :QWidget
    instance :'ScreenManager' = None

    def __init__(self):
        super().__init__()
        if self.instance is not None:
            raise RuntimeError('There cant be more than two screen managers!')

        self.instance = self
        self.current_screen = QWidget()

    def set_screen(self, new_screen :QWidget):
        self.current_screen = new_screen
        self.screen_changed.emit(self.current_screen)

    @staticmethod
    def setup():
        ScreenManager.instance = ScreenManager()
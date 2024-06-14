from PySide6.QtWidgets import QApplication
from ui.window import Window
from ui.screen_manager import ScreenManager
from ui.screens.main_menu import MainMenu
from networking.client.client import Client


app = QApplication()
Client.setup()
ScreenManager.setup()

window = Window()
ScreenManager.instance.set_screen(MainMenu())

window.show()
exit(app.exec())
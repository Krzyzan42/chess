from PySide6 import QtAsyncio
from PySide6.QtWidgets import QApplication
from ui.window import Window
from ui.screen_manager import ScreenManager
from ui.screens.main_menu import MainMenu
from networking.client.client import Client
import logging


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    app = QApplication()
    Client.setup()
    ScreenManager.setup()

    window = Window()
    ScreenManager.instance.set_screen(MainMenu())
    window.show()
    QtAsyncio.run(debug=True)

if __name__ == '__main__':
    main()
from PySide6 import QtAsyncio
from PySide6.QtWidgets import QApplication
from ui.window import Window
from ui.screen_manager import ScreenManager
from ui.screens.chess_vs_friend import ChessVsFriend
from networking.client.client import Client
import logging


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    app = QApplication()
    Client.setup()
    ScreenManager.setup()

    window = Window()
    ScreenManager.instance.set_screen(ChessVsFriend())
    window.show()
    QtAsyncio.run(debug=True)

if __name__ == '__main__':
    main()
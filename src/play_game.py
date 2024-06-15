from PySide6 import QtAsyncio
from PySide6.QtWidgets import *
from ui.window import Window
from ui.screen_manager import ScreenManager
from ui.screens import *
from networking.client.client import Client
from networking.common import *
from networking.server.models import init_db
import logging
import sys
from asyncio import ensure_future, sleep
import time
from networking import settings

async def create_room():
    client = Client.instance
    await client.connect_to_server(settings.server_ip, settings.server_port)
    # await client.auth.login('asdf', 'asdf')
    ScreenManager.instance.set_screen(LoginScreen())
    

async def join_room():
    client = Client.instance
    await client.connect_to_server(settings.server_ip, settings.server_port)
    await client.auth.login('asdfg', 'asdfg')
    ScreenManager.instance.set_screen(OnlineMenu())

async def spectate_room():
    client = Client.instance
    await client.connect_to_server(settings.server_ip, settings.server_port)
    await client.auth.login('asdfgh', 'asdfgh')
    ScreenManager.instance.set_screen(OnlineMenu())



def main():
    host = False
    spectate = False
    if sys.argv[1] == 'host':
        host = True
    elif sys.argv[1] == 'guest':
        host = False
    elif sys.argv[1] == 'spectate':
        spectate = True
    else:
        raise RuntimeError()


    logging.getLogger().setLevel(logging.DEBUG)
    app = QApplication()
    Client.setup()
    ScreenManager.setup()

    window = Window()
    play_btn = QPushButton(sys.argv[1])
    if host and not spectate:
        window.setGeometry(1, 1, window.width(), window.height())
        play_btn.clicked.connect(lambda: ensure_future(create_room()))
    elif not host and not spectate:
        window.setGeometry(900, 1, window.width(), window.height())
        play_btn.clicked.connect(lambda: ensure_future(join_room()))
    else:
        window.setGeometry(1, 500, 100, 100)
        play_btn.clicked.connect(lambda: ensure_future(spectate_room()))

    ScreenManager.instance.set_screen(play_btn)
    window.show()
    QtAsyncio.run(debug=True)

if __name__ == '__main__':
    main()
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.client.client import Client, ClientState, ConnectionState

class ConnectCoroutine(QObject):
    done = Signal(bool, str)
    dialog :QDialog = None

    def __init__(self):
        super().__init__()

    def start_(self):
        client = Client.instance
        if client._state.state == ConnectionState.CONNECTED:
            print('emmiting in start')
            self.done.emit(True, None)
            return

        client.state_changed.connect(self.client_state_changed)
        # client.state_changed.connect(lambda x: print('what'))
        # client.state_changed.connect(lambda x: self.client_state_changed(x))
        client.connect_to_server()

    @Slot(ClientState)
    def client_state_changed(self, client_state :ClientState):
        print(f'Coroutine caught: {client_state}')
        if client_state.state == ConnectionState.CONNECTED:
            print('emitting true')
            self.done.emit(True, None)
        elif client_state.state == ConnectionState.DISCONNECTED:
            print('emitting false')
            self.done.emit(False, client_state.error_msg)

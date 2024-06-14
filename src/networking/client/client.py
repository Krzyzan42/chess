from PySide6.QtCore import *
from PySide6.QtCore import QObject, QTimerEvent
from networking.client import *
from networking.common import Connection, Message
from networking.client.connect_thread import ConnectThread
from networking import settings


class Client(QObject):
    state_changed = Signal(ClientState)
    msg_recieved = Signal(Message)
    instance :'Client' = None
    
    _connection_thread :ConnectThread
    _state :ClientState
    _connection :Connection
    _server_ip :str
    _server_port :int

    def __init__(self):
        super().__init__()
        if self.instance is not None:
            raise RuntimeError('Cant have more than two client instances at once!')

        self.instance = self
        self._server_port = settings.server_port
        self._server_ip = settings.server_ip
        self._connection_thread = None
        self._state = ClientState(ConnectionState.DISCONNECTED)
        self._connection = None
        self.startTimer(16)

    @staticmethod
    def setup():
        Client.instance = Client()

    def connect_to_server(self):
        if self._state.state == ConnectionState.DISCONNECTED:
            self._connection_thread = ConnectThread(self._server_ip, self._server_port)
            self._connection_thread.result_ready.connect(self._connection_result)
            self._connection_thread.start()

            self._state = ClientState(ConnectionState.CONNECTING)
            self.state_changed.emit(self._state)

    def disconnect_from_server(self):
        if self._state.state == ConnectionState.CONNECTED:
            self._connection.close()
            self._connection = None
            self._state = ClientState(ConnectionState.DISCONNECTED)
            self.state_changed.emit(self._state)

    @Slot(Message)
    def send_msg(self, msg :Message):
        if self._state.state == ConnectionState.CONNECTED:
            self._connection.out_queue.put(msg)
        
    def timerEvent(self, _: QTimerEvent) -> None:
        if self._state.state != ConnectionState.CONNECTED:
            return
        if not self._connection.is_alive():
            self.disconnect_from_server()
            return
        
        while not self._connection.in_queue.empty():
            msg = self._connection.in_queue.get_nowait()
            self.msg_recieved.emit(msg)

    def _connection_result(self, success :bool, error_msg :str | None):
        if success:
            print('Client succesfully connected', flush=True)
            self._state = ClientState(ConnectionState.CONNECTED)
            self._connection = Connection(self._connection_thread.result_socket)
            self._connection_thread = None
            self.state_changed.emit(self._state)
        else:
            print(f'Client failed to connect. Reason: {error_msg}', flush=True)
            self._state = ClientState(ConnectionState.DISCONNECTED, error_msg)
            self._connection = None
            self._connection_thread = None
            self.state_changed.emit(self._state)
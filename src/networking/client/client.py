from PySide6.QtCore import *
from networking.common import *
import asyncio
from networking.client.auth import Auth
from networking.client.room import Room
 
class Client(QObject):
    connected = Signal()
    disconnected = Signal(str)
    msg_recieved = Signal(Message)

    instance :'Client'
    auth :Auth
    room :Room

    is_connected :bool

    _connection :ClientConnection

    def __init__(self) -> None:
        super().__init__()
        self._connection = ClientConnection(on_disconnect=self._on_disconnect)
        self.auth = Auth(self._connection)
        self.room = Room(self._connection)
        self.is_connected = False
        Client.instance = self

        self.msg_recieved.connect(self.auth.msg_recieved)
        self.msg_recieved.connect(self.room.msg_recieved)

    @staticmethod
    def setup():
        Client.instance = Client()

    async def connect_to_server(self, host :str, port :int) -> str | None:
        if self.is_connected:
            return
            
        success, error = await self._connection.connect(host, port)
        if success:
            self._read_task = asyncio.create_task(self._run())
            self.is_connected = True
            self.connected.emit()
        else:
            return error

    async def disconnect_from_server(self):
        self.is_connected = False
        self._connection.close()

    async def _run(self):
        try:
            while True:
                msg = await self._connection.pop_message()
                self.msg_recieved.emit(msg) 
        except SocketError as e:
            return

    def _on_disconnect(self, msg :str | None):
        self.is_connected = False
        self.disconnected.emit(msg)
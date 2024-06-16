import asyncio 
from . import SocketError, SocketWriter, SocketReader
from networking.common.message import Message
import socket
from queue import Queue


class MsgSocket:
    _reader :SocketReader
    _writer :SocketWriter
    _in_msg :Queue
    _out_msg :Queue

    _read_future :asyncio.Future

    def __init__(self):
        self._in_msg = Queue()
        self._out_msg = Queue()
        self._read_future = None

    async def update(self):
        while True:
            if not self._in_msg.empty() and self._read_future is not None:
                self._read_future.set_result(self._in_msg.get())
                self._read_future = None
            await asyncio.sleep(0.01)

    # Can raise exception
    async def connect(self, host :str, port :int):
        try:
            self._update_task = asyncio.create_task(self.update())
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            self._reader = SocketReader(daemon=True)
            self._reader.conn = sock
            self._reader.incoming_messages = self._in_msg
            self._reader.start()
            self._writer = SocketWriter(daemon=True)
            self._writer.conn = sock
            self._writer.outgoing_messages = self._out_msg
            self._writer.start()
        except NotImplementedError:
            raise SocketError(f'Failed to connect. Not implemented')
        except Exception as e:
            raise SocketError(f'Failed to connect {str(e)}')

    # Can raise exception
    async def read(self) -> Message:
        self._read_future = asyncio.get_event_loop().create_future()
        result = await self._read_future
        return result

    def write(self, message :Message):
        self._out_msg.put(message)

    async def drain(self):
        pass

    def close(self):
        if self._writer:
            self._writer.conn.close()
            self._reader = None
            self._writer = None
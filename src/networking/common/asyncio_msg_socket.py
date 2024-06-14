import asyncio 
import pickle
from . import SocketError
from networking.common.message import Message

class AsyncioMsgSocket:
    _reader :asyncio.StreamReader = None
    _writer :asyncio.StreamWriter = None

    def __init__(self, reader = None, writer = None):
        self._reader = reader
        self._writer = writer

    # Can raise exception
    async def connect(self, host :str, port :int):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            self._reader = reader
            self._writer = writer
        except:
            raise SocketError('Failed to connect')

    # Can raise exception
    async def read(self) -> Message:
        if not self._reader:
            raise SocketError('Not connected')

        try:
            data = await self._reader.readexactly(4)
            payload_size = int.from_bytes(data, 'big')
            msg_data = await self._reader.readexactly(payload_size)
            msg :Message = pickle.loads(msg_data)
            return msg
        except Exception as e:
            raise SocketError('Failed to read')

    def write(self, message :Message):
        if not self._reader:
            raise SocketError('Not connected')

        try:
            msg_data = pickle.dumps(message)
            payload_size = len(msg_data)
            data_sent = int.to_bytes(payload_size, 4, 'big') + msg_data 
            self._writer.write(data_sent)
        except Exception as e:
            raise SocketError('Failed to write')

    async def drain(self):
        if self._writer:
            await self._writer.drain()

    def close(self):
        if self._writer:
            self._writer.close()
            self._reader = None
            self._writer = None
import asyncio
from . import AsyncioMsgSocket, SocketError
from networking.common.message import *

class ServerConnection:
    _socket :AsyncioMsgSocket
    _is_alive :bool
    _in_messages :asyncio.Queue
    _read_task :asyncio.Task

    def __init__(self, reader, writer, msg_queue):
        self._socket = AsyncioMsgSocket(reader, writer)
        self._is_alive = True
        self._read_task = asyncio.create_task(self._read_and_queue())
        self._in_messages = msg_queue

    def send(self, msg :Message):
        try:
            self._socket.write(msg)
        except SocketError:
            self.close()

    async def drain(self):
        await self._socket.drain()

    def is_alive(self):
        return self._is_alive

    def close(self):
        if self._is_alive:
            print(f'Closing connection', flush=True)
        self._is_alive = False
        self._socket.close()
        if self._read_task is not None:
            self._read_task.cancel()
            self._read_task = None

    async def _read_and_queue(self):
        while True:
            try:
                msg = await self._socket.read()
                msg.owner = self
                self._in_messages.put_nowait(msg)
            except SocketError as e:
                self.close()
                break
            except asyncio.CancelledError as e:
                break
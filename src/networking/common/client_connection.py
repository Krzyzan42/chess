import asyncio
from networking.common.message import *
from typing import Callable
from uuid import uuid4
from . import SocketError, MsgSocket


# Everthing except close may raise an exception
class ClientConnection:
    _msg_socket :MsgSocket
    _disconnect_callback :Callable[[str], None]
    _connect_callback :Callable[[], None]
    _incoming_messages :asyncio.Queue[Message]
    _pending_responses :dict[str, asyncio.Future]
    _is_connected :bool
    _reader_task :asyncio.Task

    def __init__(self, on_disconnect = None, _on_connect = None):
        self._msg_socket = MsgSocket()
        self._connect_callback = _on_connect
        self._disconnect_callback = on_disconnect
        self._incoming_messages = asyncio.Queue()
        self._pending_responses = {}
        self._is_connected = False
        self._reader_task = None

    async def connect(self, host :str, port :int) -> tuple[bool, str]:
        try:
            await self._try_connect(host, port)
            return True, None
        except SocketError as e:
            return False, e.reason

    async def pop_message(self):
        if not self._is_connected:
            raise SocketError('Not connected')

        result = await self._incoming_messages.get()
        if isinstance(result, SocketError):
            raise result
        else:
            return result

    def message_available(self):
        return self._incoming_messages.qsize() > 0

    async def send_request(self, msg: Message) -> Message:
        try:
            return await self._try_send_request(msg)
        except SocketError as e:
            self.close(e.reason)
            raise e

    async def send_message(self, msg :Message):
        try:
            self._msg_socket.write(msg)
            await self._msg_socket.drain()
        except SocketError as e:
            print(str(e))
            self.close()
            raise e

    def close(self, reason :str = ''):
        if not self._is_connected:
            return

        self._msg_socket.close()
        self._is_connected = False
        self._reader_task.cancel()
        for future in self._pending_responses.values():
            future.set_exception(SocketError(reason))
        self._pending_responses.clear()
        if self._disconnect_callback:
            self._disconnect_callback(reason)
        while self._incoming_messages.qsize() > 0:
            self._incoming_messages.get()
        self._incoming_messages.put(SocketError(reason))

    def set_disconnect_callback(self, callback):
        self._disconnect_callback = callback

    def set_connect_callback(self, callback):
        self._connect_callback = callback

    async def _try_connect(self, host :str, port :int):
        await self._msg_socket.connect(host, port)
        
        self._is_connected = True
        while self._incoming_messages.qsize() > 0: # Clear SocketError if any
            self._incoming_messages.get()

        self._reader_task = asyncio.create_task(self._read_and_queue())
        if self._connect_callback:
            self._connect_callback()

    async def _try_send_request(self, msg :Message) -> Message:
        msg.id = uuid4()
        future = asyncio.get_event_loop().create_future()
        self._pending_responses[msg.id] = future
        self._msg_socket.write(msg)
        await self._msg_socket.drain()
        response = await future
        return response

    async def _read_and_queue(self):
        while True:
            try:
                msg = await self._msg_socket.read()
                self._process_read_message(msg)
            except SocketError as e:
                print(str(e))
                break
            except asyncio.CancelledError as e:
                break
    
    def _process_read_message(self, msg :Message):
        if msg.id:
            future = self._pending_responses.pop(msg.id)
            future.set_result(msg)
        else:
            self._incoming_messages.put_nowait(msg)
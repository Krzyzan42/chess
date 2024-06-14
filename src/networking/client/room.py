from PySide6.QtCore import *
from PySide6.QtCore import QObject
from networking.common.message import *
from networking.common.client_connection import ClientConnection


class Room(QObject):
    left_room = Signal(str)
    joined_room = Signal(RoomInfo)
    room_updated = Signal(RoomInfo)

    current_room :RoomInfo | None
    _conn :ClientConnection

    def __init__(self, connection :ClientConnection) -> None:
        super().__init__()
        self._conn = connection

    async def create_room(self, name :str) -> Response:
        return await self._conn.send_request(RoomCreateRequest(name))

    async def join_room(self, id :int) -> Response:
        return await self._conn.send_request(JoinRoomRequest(id))
    
    async def leave_room(self) -> Response:
        return await self._conn.send_request(LeaveRoomRequest())

    async def start_game(self) -> Response:
        return await self._conn.send_request(StartGameRequest())

    async def list_rooms(self) -> list[RoomInfo]:
        return await self._conn.send_request(ListRoomsRequest())

    def process_message(self, msg :Message):
        if msg.msg_type != MSG_ROOM_UPDATED:
            return
        msg :RoomUpdatedMsg = msg

        self.current_room = msg.room
        if msg.joined:
            self.joined_room.emit(msg.room)
        elif msg.kick_msg or msg.room is None:
            self.left_room.emit(msg.kick_msg)

        self.room_updated.emit(msg.room)
        print(msg)
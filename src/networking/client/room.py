from PySide6.QtCore import *
from PySide6.QtCore import QObject
from networking.common.message import *
from networking.common.client_connection import ClientConnection


class Room(QObject):
    left_room = Signal(str)
    joined_room = Signal(RoomInfo)
    room_updated = Signal(RoomInfo)

    current_room :RoomInfo | None
    is_spectating :bool | None
    _conn :ClientConnection

    def __init__(self, connection :ClientConnection) -> None:
        super().__init__()
        self._conn = connection
        self.current_room = None
        self.is_spectating = False

    async def create_room(self, name :str) -> Response:
        return await self._conn.send_request(RoomCreateRequest(name))

    async def join_room(self, id :int, spectate = False) -> Response:
        return await self._conn.send_request(JoinRoomRequest(id, spectate=spectate))
    
    async def leave_room(self) -> Response:
        return await self._conn.send_request(LeaveRoomRequest())

    async def start_game(self) -> Response:
        return await self._conn.send_request(StartGameRequest())

    async def list_rooms(self) -> list[RoomInfo]:
        result :RoomListResponse = await self._conn.send_request(ListRoomsRequest())
        return result.rooms

    def msg_recieved(self, msg :Message):
        handlers = {
            MSG_ROOM_JOINED: self._handle_room_joined,
            MSG_ROOM_UPDATED: self._handle_room_updated,
            MSG_ROOM_LEFT: self._handle_room_left,
        }
        if msg.msg_type in handlers:
            handlers[msg.msg_type](msg)

    def _handle_room_joined(self, msg :RoomJoinedMsg):
        self.current_room = msg.room
        self.is_spectating = msg.spectates
        self.joined_room.emit(msg.room)

    def _handle_room_updated(self, msg :RoomUpdatedMsg):
        self.current_room = msg.room
        self.room_updated.emit(msg.room)

    def _handle_room_left(self, msg :RoomLeftMsg):
        self.current_room = None
        self.is_spectating = False
        self.left_room.emit(msg.kick_msg)
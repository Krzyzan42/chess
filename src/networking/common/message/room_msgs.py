from .message import *

@dataclass
class RoomInfo:
    room_id :int
    room_name :str
    host_name :str
    guest_name :str  | None = None

@dataclass
class RoomCreateRequest(Message):
    msg_type = MSG_ROOM_CREATE_REQUEST
    room_name :str
    id :str

@dataclass
class ListRoomsRequest(Message):
    msg_type = MSG_ROOM_LIST_REQUEST
    id :str

@dataclass
class RoomListResponse(Message):
    msg_type = MSG_ROOM_LIST_RESPONSE
    rooms :list[RoomInfo]
    id :str

    def __str__(self) -> str:
        result = ''
        for room in self.rooms:
            result += f'Room "{room.room_name}". ID: {room.room_id} \n'
        return result

@dataclass
class JoinRoomRequest(Message):
    msg_type = MSG_JOIN_ROOM_REQUEST
    room_id :int
    id :str

@dataclass
class LeaveRoomRequest(Message):
    msg_type = MSG_LEAVE_ROOM_REQUEST
    id :str

@dataclass 
class StartGameRequest(Message):
    msg_type = MSG_START_GAME_REQUEST
    id :str

@dataclass
class RoomUpdatedMsg(Message):
    msg_type = MSG_ROOM_UPDATED
    room :RoomInfo | None = None
    kick_msg :str | None = None
    someone_joined_msg :str | None = None
    someone_left_msg :str | None = None
    joined :bool | None = None
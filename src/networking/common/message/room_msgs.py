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

@dataclass
class ListRoomsRequest(Message):
    msg_type = MSG_LIST_ROOMS_REQUEST

@dataclass
class JoinRoomRequest(Message):
    msg_type = MSG_JOIN_ROOM_REQUEST
    room_id :int

@dataclass
class LeaveRoomRequest(Message):
    msg_type = MSG_LEAVE_ROOM_REQUEST

@dataclass
class RoomInfoRequest(Message):
    msg_type = MSG_ROOM_INFO_REQUEST


@dataclass
class RoomListMsg(Message):
    msg_type = MSG_ROOM_LIST
    rooms :list[RoomInfo]

    def __str__(self) -> str:
        result = ''
        for room in self.rooms:
            result += f'Room "{room.room_name}". ID: {room.room_id} \n'
        return result

@dataclass
class RoomJoinMsg(Message):
    msg_type = MSG_ROOM_JOIN
    success :bool
    room_info :RoomInfo | None = None
    error_str :str | None = None

@dataclass
class RoomInfoMsg(Message):
    msg_type = MSG_ROOM_INFO
    is_in_room :bool
    room :RoomInfo | None = None

@dataclass
class RoomLeftMessage(Message):
    msg_type = MSG_ROOM_LEFT
    reason :str | None = None
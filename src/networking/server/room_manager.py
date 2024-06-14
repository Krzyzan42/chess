import random
from dataclasses import dataclass
from networking.common import *
from networking.server.models import User
from . import LoginManager

@dataclass
class Room:
    id :int
    name :str
    host :Connection
    host_username :str
    guest :Connection = None
    guest_username :str = None

    def to_room_info(self) -> RoomInfo:
        return RoomInfo(self.id, self.name, self.host_username, self.guest_username)

    def __str__(self) -> str:
        guest_str = ''
        if self.guest_username:
            guest_str = f'Guest {self.guest_username}.'
        return f'Room {self.name}. ID: {self.id}. Host {self.host_username}. {guest_str}'


class RoomManager:
    rooms :dict[int, Room]
    login_mng :LoginManager

    def __init__(self) -> None:
        self.rooms = {}
        self.login_mng = LoginManager.instance

    def process_message(self, msg :Message):
        processors = {
            MSG_ROOM_CREATE_REQUEST: self._process_room_create_request,
            MSG_LIST_ROOMS_REQUEST: self._process_room_list_request,
            MSG_JOIN_ROOM_REQUEST: self._process_join_room_request,
            MSG_LEAVE_ROOM_REQUEST: self._process_leave_room_request,
            MSG_ROOM_INFO_REQUEST: self._process_room_info_request,
        }
        if msg.msg_type in processors:
            processors[msg.msg_type](msg)

    def update(self):
        pass

    def cleanup(self, dead_conns :list[Connection]):
        for conn in dead_conns:
            room = self._get_conn_room(conn)
            if room:
                self._remove_conn_from_room(room, conn)

    def _process_room_create_request(self, msg :RoomCreateRequest):
        if not self.login_mng.is_logged(msg.owner):
            msg.owner.out_queue.put(RoomJoinMsg(False, error_str='You need to log in to create a room!'))
            return
        user = self.login_mng.get_user(msg.owner)

        room = Room(
            id = random.randint(0, 100000),
            name = msg.room_name,
            host = msg.owner,
            host_username = user.username
        )
        self.rooms[room.id] = room
        msg.owner.out_queue.put(RoomJoinMsg(True, room_info=room.to_room_info()))
        print(f'Room {msg.room_name} created. ID: {room.id}')

    def _process_room_list_request(self, msg :Message):
        room_infos = []
        for room in self.rooms.values():
            room_infos.append(room.to_room_info())

        msg.owner.out_queue.put(RoomListMsg(room_infos))

    def _process_join_room_request(self, msg :JoinRoomRequest):
        if not self.login_mng.is_logged(msg.owner):
            msg.owner.out_queue.put(RoomJoinMsg(False, error_str='You need to log in to join a room!'))
            return
        user = self.login_mng.get_user(msg.owner)
        id = msg.room_id
        room = self.rooms[id]
        room.guest = msg.owner
        room.guest_username = user.username
        room.host.out_queue.put(RoomInfoMsg(True, room.to_room_info()))
        room.guest.out_queue.put(RoomJoinMsg(True, room.to_room_info()))

    def _process_room_info_request(self, msg :RoomInfoRequest):
        room = self._get_conn_room(msg.owner)
        if room:
            msg.owner.out_queue.put(RoomInfoMsg(
                True,
                room.to_room_info(),
            ))
        else:
            msg.owner.out_queue.put(RoomInfoMsg(False))

    def _process_leave_room_request(self, msg :LeaveRoomRequest):
        room = self._get_conn_room(msg.owner)
        if room is None:
            msg.owner.out_queue.put(RoomLeftMessage())
            return
        self._remove_conn_from_room(room, msg.owner)
    
    def _remove_conn_from_room(self, room :Room, conn :Connection):
        if room.guest == conn:
            room.guest = None
            room.host.out_queue.put(RoomInfoMsg(room.to_room_info()))
            conn.out_queue.put(RoomLeftMessage())
        elif room.host == conn:
            if room.guest:
                room.guest.out_queue.put(RoomLeftMessage('Host left the room'))
            self.rooms.pop(room.id)
            print(f'Removing {room}')
            conn.out_queue.put(RoomLeftMessage())
        else:
            raise RuntimeError('what')


    def _get_conn_room(self, conn :Connection) -> Room | None:
        for room in self.rooms.values():
            if room.host == conn or room.guest == conn:
                return room
import random
from dataclasses import dataclass
from networking.common import *
from networking.server.models import User
from . import LoginManager

@dataclass
class Room:
    id :int
    name :str
    host :ServerConnection
    host_username :str
    guest :ServerConnection = None
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
            MSG_ROOM_LIST_REQUEST: self._process_room_list_request,
            MSG_JOIN_ROOM_REQUEST: self._process_join_room_request,
            MSG_LEAVE_ROOM_REQUEST: self._process_leave_room_request,
        }
        if msg.msg_type in processors:
            processors[msg.msg_type](msg)

    def update(self):
        conns_to_remove = [] 
        for room in self.rooms.values():
            c1 = room.host
            c2 = room.guest
            if not c1.is_alive() or not self.login_mng.is_logged(c1):
                conns_to_remove.append(c1)
            elif c2:
                if not c2.is_alive() or not self.login_mng.is_logged(c2): 
                    conns_to_remove.append(c2)

        for conn in conns_to_remove:
            room = self._get_conn_room(conn)
            if room is not None:
                self._remove_conn_from_room(room, conn)

    def _process_room_create_request(self, msg :RoomCreateRequest):
        if not self.login_mng.is_logged(msg.owner):
            msg.owner.send(Response(msg.id, False, 'You need to log in to create a room!'))
        elif len(msg.room_name) < 3:
            msg.owner.send(Response(msg.id, False, 'Room name needs to have at least 3 letters'))
        elif self._room_exists(msg.room_name):
            msg.owner.send(Response(msg.id, False, 'Room with that name already exists'))
        else:
            user = self.login_mng.get_user(msg.owner)
            room = Room(
                id = random.randint(0, 100000),
                name = msg.room_name,
                host = msg.owner,
                host_username = user.username
            )
            self.rooms[room.id] = room
            msg.owner.send(Response(msg.id, True))
            msg.owner.send(RoomUpdatedMsg(room.to_room_info(), joined=True))
            print(f'Room {msg.room_name} created. ID: {room.id}')
    
    def _room_exists(self, name):
        return name in [room.name for room in self.rooms.values()]

    def _process_room_list_request(self, msg :Message):
        room_infos = []
        for room in self.rooms.values():
            room_infos.append(room.to_room_info())

        msg.owner.send(RoomListResponse(room_infos, msg.id))

    def _process_join_room_request(self, msg :JoinRoomRequest):
        room = self.rooms.get(msg.room_id, None)
        if not self.login_mng.is_logged(msg.owner):
            msg.owner.send(Response(msg.id, False, 'You need to be logged in to join a room'))
        elif not room:
            msg.owner.send(Response(msg.id, False, 'Room doesnt exist'))
        elif room.guest is not None:
            msg.owner.send(Response(msg.id, False, 'Room is full'))
        else:
            user = self.login_mng.get_user(msg.owner)
            id = msg.room_id
            room = self.rooms[id]
            room.guest = msg.owner
            room.guest_username = user.username

            room.host.send(RoomUpdatedMsg(room.to_room_info(), someone_joined_msg=user.username))
            room.guest.send(RoomUpdatedMsg(room.to_room_info(), joined=True))
            msg.owner.send(Response(msg.id, True))

    def _process_leave_room_request(self, msg :LeaveRoomRequest):
        room = self._get_conn_room(msg.owner)
        if room is None:
            msg.owner.send(Response(msg.id, False, 'Room doesnt exist'))
        else:
            self._remove_conn_from_room(room, msg.owner)
            msg.owner.send(Response(msg.id, True))
    
    def _remove_conn_from_room(self, room :Room, conn :ServerConnection):
        if room.guest == conn:
            user_leaving = room.guest_username
            room.guest = None
            room.guest_username = None
            room.host.send(RoomUpdatedMsg(room.to_room_info(), someone_left_msg=user_leaving))
            conn.send(RoomUpdatedMsg(None))
        elif room.host == conn:
            if room.guest:
                room.guest.send(RoomUpdatedMsg(None, kick_msg='Host left the room'))
            room.host.send(RoomUpdatedMsg(None))
            self.rooms.pop(room.id)
            print(f'Removing {room}')
        else:
            print(f'Room manager trying to remove connection from room that it doesnt belong to', flush=True)
            raise RuntimeError('what')

    def _get_conn_room(self, conn :ServerConnection) -> Room | None:
        for room in self.rooms.values():
            if room.host == conn or room.guest == conn:
                return room
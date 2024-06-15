import random
from networking.common import *
from networking.server.models import User
from . import LoginManager
from . import GameManager
from . import Room

class RoomManager:
    rooms :dict[int, Room]
    login_mng :LoginManager
    game_mng :GameManager

    _waiting_games :list[tuple[ClientConnection, ClientConnection]]

    def __init__(self) -> None:
        self.rooms = {}
        self.login_mng = LoginManager.instance
        self._waiting_games = []

    def process_message(self, msg :Message):
        processors = {
            MSG_ROOM_CREATE_REQUEST: self._process_room_create_request,
            MSG_ROOM_LIST_REQUEST: self._process_room_list_request,
            MSG_JOIN_ROOM_REQUEST: self._process_join_room_request,
            MSG_LEAVE_ROOM_REQUEST: self._process_leave_room_request,
            MSG_START_GAME_REQUEST: self._process_start_game_request,
        }
        if msg.msg_type in processors:
            processors[msg.msg_type](msg)

    def update(self):
        conns_to_remove = [] 
        for room in self.rooms.values():
            spectators = room.spectators
            conns = spectators + [room.host, room.guest]
            for conn in conns:
                if not conn:
                    continue
                if not conn.is_alive() or not self.login_mng.is_logged(conn):
                    conns_to_remove.append(conn)

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
                host_username = user.username,
                spectators=[]
            )
            self.rooms[room.id] = room
            msg.owner.send(RoomJoinedMsg(room.to_room_info(), spectates=False))
            msg.owner.send(Response(msg.id, True))
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
        elif room.guest is not None and msg.spectate is False:
            msg.owner.send(Response(msg.id, False, 'Room is full'))
        else:
            user = self.login_mng.get_user(msg.owner)
            id = msg.room_id
            room = self.rooms[id]
            if not msg.spectate:
                room.guest = msg.owner
                room.guest_username = user.username
            else:
                room.spectators.append(msg.owner)

            room.host.send(RoomUpdatedMsg(room.to_room_info()))
            for conn in room.spectators:
                conn.send(RoomUpdatedMsg(room.to_room_info()))
            msg.owner.send(RoomJoinedMsg(room.to_room_info(), spectates=msg.spectate))
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
            room.guest = None
            room.guest_username = None
            room.host.send(RoomUpdatedMsg(room.to_room_info()))
            conn.send(RoomLeftMsg(None))
        elif room.host == conn:
            if room.guest:
                room.guest.send(RoomLeftMsg(None, kick_msg='Host left the room'))
            room.host.send(RoomLeftMsg(None))
            self.rooms.pop(room.id)
            print(f'Removing {room}')
        elif conn in room.spectators:
            room.spectators.remove(conn)
            conn.send(RoomLeftMsg())
        else:
            print(f'Room manager trying to remove connection from room that it doesnt belong to', flush=True)
            raise RuntimeError('what')

    def _get_conn_room(self, conn :ServerConnection) -> Room | None:
        for room in self.rooms.values():
            if room.host == conn or room.guest == conn:
                return room

    def _process_start_game_request(self, msg :StartGameRequest):
        room = self._get_conn_room(msg.owner)
        if not room:
            msg.owner.send(Response(msg.id, False, 'You need to be in a room to start a game!'))
        elif room.guest is None or room.host is None:
            msg.owner.send(Response(msg.id, False, 'There need to be two people in the room!'))
        elif room.host is not msg.owner:
            msg.owner.send(Response(msg.id, False, 'Only host can start the game!'))
        else:
            self._waiting_games.append((room.host, room.guest))
            self.rooms.pop(room.id)
            self.game_mng.start_game(room)
            msg.owner.send(Response(msg.id, True))
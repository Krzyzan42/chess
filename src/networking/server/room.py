from networking.common import *

@dataclass
class Room:
    id :int
    name :str
    host :ServerConnection
    host_username :str
    spectators :list[ServerConnection]
    guest :ServerConnection = None
    guest_username :str = None

    def to_room_info(self) -> RoomInfo:
        return RoomInfo(self.id, self.name, self.host_username, self.guest_username)

    def __str__(self) -> str:
        guest_str = ''
        if self.guest_username:
            guest_str = f'Guest {self.guest_username}.'
        return f'Room {self.name}. ID: {self.id}. Host {self.host_username}. {guest_str}'
from PySide6.QtCore import *
from networking.common import *
from networking.client import *

class LoadRoomsCoroutine(QObject):
    done = Signal(list[RoomInfo])

    def start(self):
        client = Client.instance
        client.msg_recieved.connect(self.msg_recieved)
        client.send_msg(ListRoomsRequest())

    @Slot(Message)
    def msg_recieved(self, msg :Message):
        if msg.msg_type == MSG_ROOM_LIST:
            msg :RoomListMsg = msg
            self.done.emit(msg.rooms)
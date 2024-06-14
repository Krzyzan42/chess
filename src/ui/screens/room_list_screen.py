from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui.room_list_widget import RoomListWidget
from ui.loading_dialog import LoadingDialog
from ui import ScreenManager

class RoomListScreen(QWidget):
    _is_refreshing :bool
    _is_joining :bool
    
    def __init__(self):
        super().__init__()
        self._setup_widgets()
        Client.instance.msg_recieved.connect(self._msg_recieved)

        self._is_joining = False
        self._is_refreshing = False
        self._update_ui()

        self._refresh()

    def _setup_widgets(self):
        layout = QVBoxLayout()
        self.back_btn = QPushButton('Back')
        self.refresh_btn = QPushButton('Refresh')
        self.join_btn = QPushButton('Join')
        self.room_list = RoomListWidget()
        
        layout.addWidget(self.back_btn)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.join_btn)
        layout.addWidget(self.room_list)
        self.setLayout(layout)

        self.back_btn.pressed.connect(self._go_back)
        self.refresh_btn.pressed.connect(self._refresh)
        self.join_btn.pressed.connect(self._join)

    def _go_back(self):
        from ui.screens import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())

    def _update_ui(self):
        if self._is_joining or self._is_refreshing:
            self.refresh_btn.setEnabled(False)
            self.join_btn.setEnabled(False)
        else:
            self.refresh_btn.setEnabled(True)
            self.join_btn.setEnabled(True)
        
    def _refresh(self):
        self._is_refreshing = True
        self._update_ui()
        Client.instance.send_msg(ListRoomsRequest())

    def _join(self):
        room = self.room_list.get_selected_room()
        if room is None:
            return

        self._is_joining = True
        self._update_ui()
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()

        Client.instance.send_msg(JoinRoomRequest(room.room_id))

    def _msg_recieved(self, msg :Message):
        print(msg)
        if msg.msg_type == MSG_ROOM_LIST:
            self._room_list_msg_recieved(msg)
        elif msg.msg_type == MSG_ROOM_JOIN:
            self._room_join_msg_recieved(msg)

    def _room_list_msg_recieved(self, msg :RoomListMsg):
        print(f'Rooms: {msg.rooms}')
        self._is_refreshing = False
        self._update_ui()
        self.room_list.set_rooms(msg.rooms)

    def _room_join_msg_recieved(self, msg :RoomJoinMsg):
        self._is_joining = False
        self.loading_dialog.accept()
        print(msg)
        self._go_to_room_screen(msg.room_info)

    def _go_to_room_screen(self, room_info :RoomInfo):
        from ui import RoomScreen
        ScreenManager.instance.set_screen(RoomScreen(room_info))
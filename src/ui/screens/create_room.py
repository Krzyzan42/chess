from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui import *

class CreateRoomScreen(QWidget):
    def __init__(self):
        super().__init__()
        Client.instance.msg_recieved.connect(self.process_msg)
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()
        left_bar = QVBoxLayout()
        title = QLabel('Create room')
        title.setStyleSheet('font-size: 25px')
        self.room_name_input = QLineEdit()
        self.room_name_input.setPlaceholderText('Room name')
        cancel_btn = QPushButton('Cancel')
        create_btn = QPushButton('Create')
        left_bar.addWidget(title)
        left_bar.addWidget(self.room_name_input)
        left_bar.addWidget(cancel_btn)
        left_bar.addWidget(create_btn)
        layout.addLayout(left_bar, 25)
        layout.addStretch(75)

        self.setLayout(layout)

        cancel_btn.pressed.connect(self._cancel_pressed)
        create_btn.pressed.connect(self._create_room_pressed)

    def _cancel_pressed(self):
        from ui import OnlineMenu
        ScreenManager.instance.set_screen(OnlineMenu())
    
    def _create_room_pressed(self):
        name = self.room_name_input.text()
        Client.instance.send_msg(RoomCreateRequest(name))
        self._loading_dialog = LoadingDialog()
        self._loading_dialog.show()

    def process_msg(self, msg :Message):
        if msg.msg_type == MSG_ROOM_JOIN:
            self.process_room_join_msg(msg)

    def process_room_join_msg(self, msg :RoomJoinMsg):
        print(msg)
        self._loading_dialog.close()
        if msg.success:
            self.go_to_room_screen(msg.room_info)

    def go_to_room_screen(self, room_info):
        from ui import RoomScreen
        ScreenManager.instance.set_screen(RoomScreen(room_info))
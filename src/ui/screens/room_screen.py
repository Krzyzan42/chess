from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from ui import *
from dataclasses import dataclass

@dataclass
class State:
    room_info :RoomInfo
    is_starting :bool = False
    is_leaving :bool = False

class RoomScreen(QWidget):
    leave_btn :QPushButton
    host_lbl :QLabel
    guest_lbl :QLabel
    loading_dialog :LoadingDialog

    state :State

    def __init__(self, room_info):
        super().__init__()
        Client.instance.msg_recieved.connect(self._process_msg)
        self.create_widgets()
        self.state = State(room_info)
        self.rebuild()

    def create_widgets(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Host: '))
        self.host_lbl = QLabel()
        layout.addWidget(self.host_lbl)
        layout.addWidget(QLabel('Guest: '))
        self.guest_lbl = QLabel()
        layout.addWidget(self.guest_lbl)
        self.leave_btn = QPushButton('Leave')
        self.leave_btn.pressed.connect(self._leave_pressed)
        layout.addWidget(self.leave_btn)
        self.loading_dialog = None
        self.setLayout(layout)

    def rebuild(self):
        state = self.state
        btns_enabled = True
        dialog_msg = None
        if state.is_leaving or state.is_starting:
            btns_enabled = False
        if state.is_leaving:
            dialog_msg = 'Leaving'
        if state.is_starting:
            dialog_msg = 'Starting game'

        host_name = state.room_info.host_name
        guest_name = state.room_info.guest_name
        if guest_name is None:
            guest_name = 'Not joined'
        
        self.host_lbl.setText(f'Host: {host_name}')
        self.guest_lbl.setText(f'Guest: {guest_name}')
        self.leave_btn.setEnabled(btns_enabled)

        if dialog_msg is None:
            if self.loading_dialog:
                self.loading_dialog.accept()
                self.loading_dialog = None
        else:
            if self.loading_dialog:
                self.loading_dialog.set_message(dialog_msg)
            else:
                self.loading_dialog = LoadingDialog()
                self.loading_dialog.set_message(dialog_msg)

    def _leave_pressed(self):
        Client.instance.send_msg(LeaveRoomRequest())
        self.state.is_leaving = True
        self.rebuild()

    def _process_msg(self, msg :Message):
        print(msg)
        if msg.msg_type == MSG_ROOM_LEFT:
            self._process_left_msg(msg)
        if msg.msg_type == MSG_ROOM_INFO:
            self._process_update_msg(msg)

    def _process_left_msg(self, msg :RoomLeftMessage):
        if msg.reason:
            msg_box = QMessageBox()
            msg_box.setText(f'You left the room. Reason {msg.reason}')
            msg_box.addButton(QMessageBox.Ok)
            msg_box.exec()
        self.exit()

    def _process_update_msg(self, msg :RoomInfoMsg):
        self.state.room_info = msg.room
        self.rebuild()

    def exit(self):
        from ui import RoomListScreen
        ScreenManager.instance.set_screen(RoomListScreen())



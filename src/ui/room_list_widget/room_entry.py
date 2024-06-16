from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *

class Title(QLabel):
    pass
class Host(QLabel):
    pass
class ActiveBtn(QPushButton):
    pass

class RoomEntry(QFrame):
    spectate = Signal(RoomInfo)
    join = Signal(RoomInfo)

    _room_name :QLabel
    _host_name :QLabel
    _join_btn :QPushButton
    _room_info :RoomInfo | None

    def __init__(self):
        super().__init__()
        self.setup_widgets()

    def setup_widgets(self):
        layout = QHBoxLayout()

        info_layout = QVBoxLayout()
        self._room_name = Title()
        self._host_name = Host()
        info_layout.addWidget(self._room_name)
        info_layout.addWidget(self._host_name)

        btn_layout = QVBoxLayout()
        self._join_btn = ActiveBtn('Join')
        self._join_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self._spectate_btn = QPushButton('Spectate')
        btn_layout.addWidget(self._join_btn)
        btn_layout.addWidget(self._spectate_btn)

        layout.addLayout(info_layout)
        layout.addStretch(1)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.set_room_info(None)
        self._join_btn.pressed.connect(lambda: self.join.emit(self._room_info))
        self._spectate_btn.pressed.connect(lambda: self.spectate.emit(self._room_info))

    def set_room_info(self, info :RoomInfo | None):
        self._room_info = info
        if info is None:
            self._room_name.setText('Unknown room')
            self._host_name.setText('Hosted by: Unknown')
            self._join_btn.setEnabled(False)
            self._spectate_btn.setEnabled(False)
        else:
            self._room_name.setText(info.room_name)
            self._host_name.setText(f'Hosted by: {info.host_name}')
            self._join_btn.setEnabled(info.guest_name is None)
            self._spectate_btn.setEnabled(True)

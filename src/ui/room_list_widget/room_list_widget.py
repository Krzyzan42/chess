from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *
from . import RoomEntry

class RoomListWidget(QFrame):
    join = Signal(RoomInfo)
    spectate = Signal(RoomInfo)

    _loading_text :QLabel
    _room_list :QFrame


    def __init__(self):
        super().__init__()
        self._rooms = []
        self.setup_widgets()
    
    def setup_widgets(self):
        layout = QVBoxLayout()

        self._loading_text = QLabel('Loading...')
        self._loading_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self._loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self._room_list = QFrame()
        self._room_list.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self._room_list.setLayout(QVBoxLayout())
        self._room_list.layout().setContentsMargins(0,0,0,0)

        layout.addWidget(self._loading_text)
        layout.addWidget(self._room_list)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        
        self.set_loading()

    def set_rooms(self, rooms :list[RoomInfo]):
        while self._room_list.layout().count():
            widget = self._room_list.layout().takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()

        for room in rooms:
            room_widget = RoomEntry()
            room_widget.set_room_info(room)
            room_widget.join.connect(self.join)
            room_widget.spectate.connect(self.spectate)
            self._room_list.layout().addWidget(room_widget)
        self._room_list.layout().addStretch(1)
        if len(rooms) != 0:
            self._room_list.setVisible(True)
            self._loading_text.setVisible(False)
        else:
            self._room_list.setVisible(False)
            self._loading_text.setVisible(True)
            self._loading_text.setText('There are no rooms, but you can create one!')

    def set_loading(self):
        self._rooms.clear()
        self._room_list.setVisible(False)
        self._loading_text.setText('Loading...')
        self._loading_text.setVisible(True)
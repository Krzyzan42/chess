from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *

class RoomListWidget(QWidget):
    selection_changed = Signal(RoomInfo)

    _rooms :list[RoomInfo]

    def __init__(self):
        super().__init__()
        self.list_widget = QListWidget()
        # self.set_rooms([])

    def set_rooms(self, rooms :list[RoomInfo]):
        print(f'setting {rooms}')
        self._rooms = rooms

        self.list_widget.clear()
        for room in rooms:
            self.list_widget.addItem(room.room_name)
        self.list_widget.currentRowChanged.connect(self._selection_changed)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Room list:'))
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def set_loading(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Loading'))
        self.setLayout(layout)

    def get_selected_room(self) -> RoomInfo:
        if self.list_widget is None:
            return None

        row = self.list_widget.currentRow()
        if row == -1:
            return None
        else:
            return self._rooms[row]

    def _selection_changed(self, row):
        if row == -1:
            self.selection_changed.emit(None)
        self.selection_changed.emit(self._rooms[row])
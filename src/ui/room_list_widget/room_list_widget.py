from PySide6.QtCore import *
from PySide6.QtWidgets import *
from networking.common import *
from networking.client import *

class RoomListWidget(QWidget):
    selection_changed = Signal(RoomInfo)

    _rooms :list[RoomInfo]

    def __init__(self):
        super().__init__()
        self._rooms = []
        self.setup_widgets()
    
    def setup_widgets(self):
        layout = QVBoxLayout()
        
        self.title_lbl = QLabel('Room list:')
        self.room_list = QListWidget()
        self.loading_widget = QLabel('Loading')
        self.room_list.currentRowChanged.connect(self._selection_changed)

        layout.addWidget(self.title_lbl)
        layout.addWidget(self.room_list)
        layout.addWidget(self.loading_widget)

        self.setLayout(layout)

    def set_rooms(self, rooms :list[RoomInfo]):
        self._rooms = rooms

        self.room_list.clear()
        for room in rooms:
            self.room_list.addItem(room.room_name)

        self.room_list.setVisible(True)
        self.loading_widget.setVisible(False)

    def set_loading(self):
        self.room_list.clear()
        self._rooms.clear()
        self.room_list.setVisible(False)
        self.loading_widget.setVisible(True)

    def get_current_room(self) -> RoomInfo | None:
        index = self.room_list.currentRow()
        if index == -1:
            return None
        else:
            return self._rooms[index]

    def _selection_changed(self):
        self.selection_changed.emit(self.get_current_room())
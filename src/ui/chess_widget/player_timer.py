from PySide6.QtCore import QObject, Signal, QTimer

class PlayerTimer(QObject):
    remaining_time_changed = Signal(int)

    def __init__(self, remaining_time :int = 0) -> None:
        self.remaining_time = remaining_time
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)

    def start(self, remaining_time):
        self.set_remaining_time(remaining_time)
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def set_remaining_time(self, remaining_time :int):
        if remaining_time < 0:
            remaining_time = 0

        self.remaining_time = remaining_time

    @property
    def remaining_time(self):
        self.remaining_time

    def _on_tick(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.timer.stop()

        self.remaining_time_changed.emit(self.remaining_time)

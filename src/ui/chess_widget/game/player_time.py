from PySide6.QtCore import Signal, QObject


# Server sends predicted end time to timers
# to prevent clock desynchronization.
# This class wraps logic to calculate remaining
# time form predicted end time
class PlayerTime(QObject):
    remaining_time_changed = Signal(int)

    def set_predicted_end_time(self):
        pass

    def stop_turn(self):
        pass
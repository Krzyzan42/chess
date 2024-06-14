from enum import Enum, auto

class GameResultType(Enum):
    WHITE_WIN = 'White won'
    BLACK_WIN = 'Black won'
    DRAW = 'Draw'

class GameResult:
    end_type :GameResultType
    reason :str

    def __init__(self, end_type :GameResultType, reason :str) -> None:
        self.end_type = end_type
        self.reason = reason

    def __str__(self) -> str:
        return f'{self.end_type.value}. Reason: {self.reason}'
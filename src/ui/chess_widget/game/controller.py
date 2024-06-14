from PySide6.QtCore import QObject, Signal, Slot 
from chess import Move, Board, Square, Color
from . import PlayerTime, MoveHistory, PlayerActor, GameResult

# Offline chess controller and online chess controller
# will both derive from this class
class ChessController(QObject):
    waiting_for_move_ack = Signal()
    recieved_move_ack = Signal()
    board_changed = Signal(Board)
    game_ended = Signal(GameResult)

    white_time :PlayerTime
    black_time :PlayerTime
    move_history :MoveHistory

    @Slot(Move)
    def move(self, move :Move):
        pass

    def get_board(self) -> Board:
        pass
    
    def possible_moves(self, from_square :Square) -> list[Move]:
        pass

    @property
    def turn(self) -> Color:
        pass

    def wait_for_move(self, user_id :str):
        pass

    def start_game(self, white :PlayerActor, black :PlayerActor):
        pass

from PySide6.QtCore import QObject, Slot
from . import ChessController, MoveHistory, PlayerActor, GameResult, GameResultType
from chess import Move, Board, Square, Color, WHITE, BLACK


class OfflineController(ChessController):
    def __init__(self) -> None:
        super().__init__()
        self.board = Board()
        self.move_history = MoveHistory()
        self.white_time = None
        self.black_time = None

    @Slot(Move)
    def move(self, move :Move):
        self.board.push(move)
        self.move_history.add_move(move)
        self.board_changed.emit(self.board)

        if self.board.is_game_over():
            self.black.end_turn()
            self.white.end_turn()

            outcome = self.board.outcome()
            end_type = None
            if outcome.winner == WHITE:
                end_type = GameResultType.WHITE_WIN
            elif outcome.winner == BLACK:
                end_type = GameResultType.BLACK_WIN
            else:
                end_type = GameResultType.DRAW
            result = GameResult(end_type, outcome.termination.name)
            self.game_ended.emit(result)
            return
        else:
            if self.board.turn == WHITE:
                self.black.end_turn()
                self.white.take_control()
            else:
                self.white.end_turn()
                self.black.take_control()

    def get_board(self) -> Board:
        return self.board

    def possible_moves(self, from_square: Square) -> list[Move]:
        possible_moves = self.board.generate_legal_moves(1 << from_square)
        return list(possible_moves)

    @property
    def turn(self) -> Color:
        return self.board.turn

    def wait_for_move(self, user_id: str):
        raise ValueError('Cant wait for move for an offline game')

    def start_game(self, white :PlayerActor, black :PlayerActor):
        self.white = white
        self.black = black
        white.take_control()

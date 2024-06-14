from PySide6.QtCore import QObject, Slot
from chess import Square, Move, square_name, Board, PAWN, WHITE, square_rank
from . import Context

class PlayerActor(QObject):
    
    def __init__(self) -> None:
        self.enabled = False
        Context.board_ui.square_clicked.connect(self.square_clicked)

    def take_control(self):
        self.enabled = True

    def end_turn(self):
        self.enabled = False
        
    @Slot(Square)
    def square_clicked(self, square :Square):
        if not self.enabled:
            return

        selection = Context.selection
        if selection.selected_square == None:
            if selection.is_selectable(square):
                selection.select(square)
            return

        if selection.selected_square == square:
            selection.deselect()
            return

        if square in selection.possible_moves():
            controller = Context.controller
            move = Move(
                selection.selected_square,
                square
            )
            board = controller.get_board()
            
            if self.is_promotion(board, move):
                Context.promotion_select.show_to_select()
                Context.promotion_select.piece_selected.connect(self.move_after_promotion)
                self._stashed_move = move
                self.enabled = False
                selection.deselect()
                return
            
            controller.move(move)
            selection.deselect()

    def move_after_promotion(self, piece_type):
        Context.promotion_select.piece_selected.disconnect(self.move_after_promotion)
        move = self._stashed_move
        move.promotion = piece_type
        Context.controller.move(move)


    def is_promotion(self, board :Board, move :Move):
        piece = board.piece_at(move.from_square)
        # Check if piece is a pawn
        if not piece or piece.piece_type != PAWN:
            return False

        turn = piece.color
        if turn == WHITE:
            if square_rank(move.from_square) != 6:
                return False
            if square_rank(move.to_square) != 7:
                return False

            return True
        else:
            if square_rank(move.from_square) != 1:
                return False
            if square_rank(move.to_square) != 0:
                return False
            
            return True
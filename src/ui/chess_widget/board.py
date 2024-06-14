from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem
from chess import Color, WHITE, BLACK
from chess_widget import (
    GameResult,
    MoveHistory,
    PlayerTimer, 
    Actor,
    ActorType,
)
from chess_widget.game import *

class Board(QWidget):
    waiting_for_server = Signal()
    recieved_server_ack = Signal()

    game_finished = Signal(GameResult)
    move_history :MoveHistory
    white_timer :PlayerTimer
    black_timer :PlayerTimer

    def __init__(self):
        super().__init__()
        self.white_actor :Actor = None
        self.black_actor :Actor = None
        self.setup_game_context()

    def set_actor(self, actor :Actor, color :Color):
        if color == WHITE:
            self.white_actor = actor
        else:
            self.black_actor = actor
        
    def start_game(self):
        if not self.white_actor or not self.black_actor:
            raise ValueError('Both actors need to be set')
        
        Context.controller.start_game(
            white=PlayerActor(),
            black=PlayerActor()
        )

    def setup_game_context(self):
        Context.params = BoardParams()
        Context.pixmaps = get_figure_pixmaps()
        Context.selection = BoardSelection()
        Context.promotion_select = PromotionSelect()

        self.controller = OfflineController()
        Context.controller = self.controller
        self.board_ui = BoardPainter()
        Context.board_ui = self.board_ui

        main_layout = QHBoxLayout()
        board_layout = QVBoxLayout()
        board_layout.addWidget(self.board_ui)
        board_layout.addWidget(Context.promotion_select)

        main_layout.addLayout(board_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.controller.game_ended.connect(self.game_finished)

        


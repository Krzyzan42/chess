from PySide6.QtCore import *
from PySide6.QtCore import QObject
from networking.common.message import *
from networking.common.client_connection import ClientConnection
import chess

class Game(QObject):
    game_started = Signal(GameState)
    game_finished = Signal(chess.Color, str)
    game_updated = Signal(GameState)
    left_spectate = Signal()

    game :GameState | None
    _conn :ClientConnection

    def __init__(self, connection :ClientConnection):
        super().__init__()
        self._conn = connection

    def msg_recieved(self, msg :Message):
        processors = {
            MSG_GAME_STARTED: self._process_game_start_msg,
            MSG_GAME_UPDATED: self._process_game_update_msg,
            MSG_GAME_ENDED: self._process_game_end_msg
        }
        if msg.msg_type in processors:
            processors[msg.msg_type](msg)

    async def move(self, move :chess.Move):
        return await self._conn.send_request(GameMoveRequest(move))

    async def send_msg(self, msg :str):
        return await self._conn.send_request(GameSendMsgRequest(msg))

    async def surrender(self):
        return await self._conn.send_request(GameSurrenderRequest())

    async def request_history(self) -> GameHistoryResponse:
        return await self._conn.send_request(GameHistoryRequest())

    async def leave(self):
        result :Response = await self._conn.send_request(LeaveSpectateRequest())
        if result.success:
            self.game = None
            self.left_spectate.emit()
        return result

    def _process_game_start_msg(self, msg :GameStarted):
        self.game = msg.state
        self.game_started.emit(self.game)

    def _process_game_update_msg(self, msg :GameUpdated):
        self.game = msg.state
        self.game_updated.emit(self.game)

    def _process_game_end_msg(self, msg :GameEnded):
        self.game_finished.emit(msg.win, msg.reason)
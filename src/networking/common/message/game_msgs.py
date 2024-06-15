from .message import *
import chess
from datetime import datetime

@dataclass
class GameState:
    hostname :str
    guestname :str
    can_move :bool
    is_spectating :bool
    messages :list[str]
    moves :list[str]
    board :chess.Board

@dataclass
class GameRecord:
    moves :list[chess.Move]
    hostname :str
    guestname :str
    win :chess.Color
    date_played :datetime



@dataclass
class GameMoveRequest(Message):
    msg_type = MSG_GAME_MOVE_REQUEST
    move :chess.Move

@dataclass
class GameSendMsgRequest(Message):
    msg_type = MSG_GAME_SEND_MSG_REQUEST
    msg :str

@dataclass
class GameSurrenderRequest(Message):
    msg_type = MSG_GAME_SURRENDER_REUQEST

@dataclass
class LeaveSpectateRequest(Message):
    msg_type = MSG_LEAVE_SPECTATE_REQUEST

@dataclass
class GameStarted(Message):
    msg_type = MSG_GAME_STARTED
    state :GameState

@dataclass
class GameUpdated(Message):
    msg_type = MSG_GAME_UPDATED
    state :GameState

@dataclass
class GameEnded(Message):
    msg_type = MSG_GAME_ENDED
    win :chess.Color | None
    reason :str

@dataclass
class GameHistoryRequest(Message):
    msg_type = MSG_GAME_HISTORY_REQUEST
    id :str

@dataclass 
class GameHistoryResponse(Message):
    msg_type = MSG_GAME_HISTORY_RESPONSE
    records :list[GameRecord]
    id :str
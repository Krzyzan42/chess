from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from networking.common import ServerConnection

MsgType = int

MESSAGES = [
    MSG_HELLO,
    MSG_ECHO_REQUEST,
    MSG_ECHO_RESPONSE,
    MSG_CLOSE,
    MSG_HEARTBEAT,
    MSG_RESPONSE,

    MSG_LOGIN_REQUEST,
    MSG_CREATE_ACC_REQUEST,
    MSG_LOGOUT_REQUEST,
    MSG_LOGIN_INFO,

    MSG_ROOM_CREATE_REQUEST,
    MSG_ROOM_LIST_REQUEST,
    MSG_ROOM_LIST_RESPONSE,
    MSG_JOIN_ROOM_REQUEST,
    MSG_LEAVE_ROOM_REQUEST,
    MSG_ROOM_INFO_REQUEST,
    MSG_ROOM_INFO_RESPONSE,
    MSG_START_GAME_REQUEST,
    MSG_ROOM_LEFT,
    MSG_ROOM_UPDATED,
    MSG_ROOM_JOINED,

    MSG_GAME_SEND_MSG_REQUEST,
    MSG_GAME_MOVE_REQUEST,
    MSG_GAME_SURRENDER_REUQEST,
    MSG_LEAVE_SPECTATE_REQUEST,

    MSG_GAME_STARTED,
    MSG_GAME_UPDATED,
    MSG_GAME_ENDED,

    MSG_GAME_HISTORY_REQUEST,
    MSG_GAME_HISTORY_RESPONSE,
] = range(1, 31)

# Message can store recieving connection as an owner.
# Useful for server side logic, where all messages
# are piped into a single queue
class Message:
    msg_type :MsgType
    owner :'ServerConnection | None' = None
    id :'str | None' = None
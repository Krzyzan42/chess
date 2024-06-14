from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from networking.common.connection import Connection

MsgType = int

MESSAGES = [
    MSG_HELLO,
    MSG_ECHO_REQUEST,
    MSG_ECHO_RESPONSE,
    MSG_CLOSE,

    MSG_LOGIN_REQUEST,
    MSG_LOGIN_RESULT,
    MSG_CREATE_ACC_REQUEST,
    MSG_CREATE_ACC_RESULT,
    MSG_LOGOUT_REQUEST,
    MSG_LOGOUT_RESULT,
    MSG_LOGIN_INFO_REQUEST,
    MSG_LOGIN_INFO_RESPONSE,

    MSG_ROOM_CREATE_REQUEST,
    MSG_LIST_ROOMS_REQUEST,
    MSG_JOIN_ROOM_REQUEST,
    MSG_LEAVE_ROOM_REQUEST,
    MSG_ROOM_INFO_REQUEST,
    MSG_START_GAME_REQUEST,
    MSG_ROOM_JOIN,
    MSG_ROOM_INFO,
    MSG_ROOM_LIST,
    MSG_ROOM_LEFT,
    MSG_GAME_STARTED,
] = range(1, 24)

# Message can store recieving connection as an owner.
# Useful for server side logic, where all messages
# are piped into a single queue
class Message:
    msg_type :MsgType
    owner :'Connection | None' 
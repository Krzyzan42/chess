from .message import *

@dataclass
class Hello(Message):
    msg_type = MSG_HELLO

@dataclass 
class EchoRequest(Message):
    msg_type = MSG_ECHO_REQUEST
    echo_str :str

@dataclass
class EchoResponse(Message):
    msg_type = MSG_ECHO_RESPONSE
    echo_str :str

@dataclass
class CloseRequest(Message):
    msg_type = MSG_CLOSE

@dataclass
class HeartbeatMsg(Message):
    msg_type = MSG_HEARTBEAT

@dataclass
class Response:
    msg_type = MSG_RESPONSE
    id :str
    success :bool
    error_str :str | None = None
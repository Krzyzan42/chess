from .message import *

@dataclass
class LoginRequest(Message):
    msg_type = MSG_LOGIN_REQUEST
    username :str
    password :str

@dataclass
class LoginResponse(Message):
    msg_type = MSG_LOGIN_RESULT
    success :bool
    username :str | None = None
    error_msg :str = None

@dataclass
class CreateAccountRequest(Message):
    msg_type = MSG_CREATE_ACC_REQUEST
    username :str
    password :str

@dataclass
class CreateAccountResponse(Message):
    msg_type = MSG_CREATE_ACC_RESULT
    success :bool
    username :str | None = None # If successfull
    error_msg :str = None

@dataclass
class LogoutRequest(Message):
    msg_type = MSG_LOGOUT_REQUEST

@dataclass
class LogoutResponse(Message):
    msg_type = MSG_LOGOUT_RESULT

@dataclass
class LoginInfoRequest(Message):
    msg_type = MSG_LOGIN_INFO_REQUEST

@dataclass
class LoginInfoResponse(Message):
    msg_type = MSG_LOGIN_INFO_RESPONSE
    is_logged :bool
    username :str | None = None
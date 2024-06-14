from .message import *

@dataclass
class LoginRequest(Message):
    msg_type = MSG_LOGIN_REQUEST
    username :str
    password :str
    id :str

@dataclass
class CreateAccountRequest(Message):
    msg_type = MSG_CREATE_ACC_REQUEST
    username :str
    password :str
    id :str

@dataclass
class LogoutRequest(Message):
    msg_type = MSG_LOGOUT_REQUEST
    id :str

@dataclass
class LoginInfo(Message):
    msg_type = MSG_LOGIN_INFO
    is_logged :bool
    username :str | None = None

    logged_in :bool | None = None
    logged_out :bool | None = None
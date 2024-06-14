from typing import Optional
from networking.common import *
from PySide6.QtCore import *


class Auth(QObject):
    logged_in = Signal(str)
    logged_out = Signal()

    current_user :str | None
    is_authenticated :bool

    def __init__(self, connection :ClientConnection) -> None:
        super().__init__()
        self.current_user = None
        self.is_authenticated = False
        self._connection = connection
    
    async def login(self, username, password) -> Response:
        return await self._connection.send_request(LoginRequest(username, password))

    async def register(self, username, password) -> Response:
        return await self._connection.send_request(CreateAccountRequest(username, password))

    async def logout(self) -> Response:
        return await self._connection.send_request(LogoutRequest())

    def msg_recieved(self, msg :Message):
        if msg.msg_type == MSG_LOGIN_INFO:
            self.update_state(msg)

    def update_state(self, login_info :LoginInfo):
        self.is_authenticated = login_info.is_logged
        self.current_user = login_info.username

        if login_info.logged_in:
            self.logged_in.emit(self.current_user)
        if login_info.logged_out:
            self.logged_out.emit()
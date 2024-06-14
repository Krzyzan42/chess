from PySide6.QtCore import *
from . import AuthState
from dataclasses import dataclass
from networking.client.client import Client, ClientState, ConnectionState
from networking.common.message import *

class Authenticator(QObject):
    login_state_changed = Signal(AuthState)
    instance :'Authenticator' = None
    state :AuthState

    _client :Client

    def __init__(self):
        super().__init__()
        if self.instance is not None:
            raise RuntimeError('There cant be more than one authenticator at the same time!')

        self.instance = self
        self.state = AuthState(False)
        self._client = Client.instance
        self._client.msg_recieved.connect(self._process_msg)
        self._client.state_changed.connect(self._connection_changed)

    @staticmethod
    def setup():
        Authenticator.instance = Authenticator()

    def _process_msg(self, msg :Message):
        msgs = {
            MSG_LOGIN_INFO_RESPONSE: self._process_login_response,
            MSG_CREATE_ACC_RESULT: self._process_register_response,
            MSG_LOGIN_INFO_RESPONSE: self._process_logout_response,
        }
        if msg.msg_type in msgs:
            msgs[msg.msg_type](msg)

    def _process_login_response(self, msg :LoginResponse):
        if msg.success:
            self.state = AuthState(True, msg.username)
        self.login_state_changed.emit(self.state)

    def _process_register_response(self, msg :CreateAccountResponse):
        if msg.success:
            self.state = AuthState(True, msg.username)
        self.login_state_changed.emit(self.state)

    def _process_logout_response(self, msg :LogoutResponse):
        self.state = AuthState(False)
        self.login_state_changed.emit(self.state)

    def _connection_changed(self, client_state :ClientState):
        if client_state.state != ConnectionState.CONNECTED:
            self.state = AuthState(False)
            self.login_state_changed.emit(self.state)

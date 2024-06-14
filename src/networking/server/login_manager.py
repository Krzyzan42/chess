from networking.common import *
from networking.server.models import User

# Keeps track of alive connections
# Manages heartbeats and hello messages
# Responds to echo requests
class LoginManager:
    logged_users :dict[Connection, User] 
    instance :'LoginManager'

    def __init__(self) -> None:
        self.logged_users = {}
        LoginManager.instance = self

    def is_logged(self, connection :Connection):
        return connection in self.logged_users

    def get_user(self, connection :Connection) -> User | None:
        if connection in self.logged_users:
            return self.logged_users[connection]
        else:
            return None

    def process_message(self, msg :Message):
        processors = {
            MSG_CREATE_ACC_REQUEST: self.process_new_acc_msg,
            MSG_LOGIN_REQUEST: self.process_login_msg,
            MSG_LOGOUT_REQUEST: self.process_logout_msg,
            MSG_LOGIN_INFO_REQUEST: self.process_login_info_msg,
        }
        if msg.msg_type in processors:
            processors[msg.msg_type](msg)

    def cleanup_connections(self, dead_connections :list[Connection]):
        for connection in dead_connections:
            if connection in self.logged_users:
                self.logged_users.pop(connection)

    # TODO: Implement password hashing
    def process_login_msg(self, msg :LoginRequest):
        user = User.get_or_none(
            username = msg.username,
            password = msg.password
        )
        if user:
            self.logged_users[msg.owner] = user
            response = LoginResponse(True, username=msg.username)
            msg.owner.out_queue.put(response)
        else:
            response = LoginResponse(False, error_msg='User not found or invalid password')
            msg.owner.out_queue.put(response)

    # TODO: make actual password/userame validation logic and password hashing
    # TODO: Prevent logging in on the same account from two connections at once
    def process_new_acc_msg(self, msg :CreateAccountRequest):
        if User.get_or_none(username=msg.username):
            response = CreateAccountResponse(False, error_msg='User with that username already exists')
            msg.owner.out_queue.put(response)
        else:
            user = User.create(
                username = msg.username,
                password = msg.password
            )
            self.logged_users[msg.owner] = user
            response = CreateAccountResponse(True, username=msg.username)
            msg.owner.out_queue.put(response)

    def process_logout_msg(self, msg :LogoutRequest):
        if msg.owner in self.logged_users:
            self.logged_users.pop(msg.owner)
        msg.owner.out_queue.put(LogoutResponse())

    def process_login_info_msg(self, msg :LoginInfoRequest):
        if msg.owner in self.logged_users:
            user = self.logged_users[msg.owner]
            msg.owner.out_queue.put(LoginInfoResponse(True, user.username))
        else:
            msg.owner.out_queue.put(LoginInfoResponse(False))
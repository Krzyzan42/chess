from networking.common import *
from networking.server.models import User

# Keeps track of alive connections
# Manages heartbeats and hello messages
# Responds to echo requests
class LoginManager:
    logged_users :dict[ServerConnection, User] 
    instance :'LoginManager'

    def __init__(self) -> None:
        self.logged_users = {}
        LoginManager.instance = self

    def is_logged(self, connection :ServerConnection):
        return connection in self.logged_users

    def is_user_logged(self, user :User):
        if user is None:
            return False
        return user in self.logged_users.values()

    def get_user(self, connection :ServerConnection) -> User | None:
        if connection in self.logged_users:
            return self.logged_users[connection]
        else:
            return None

    def process_message(self, msg :Message):
        processors = {
            MSG_CREATE_ACC_REQUEST: self.process_new_acc_msg,
            MSG_LOGIN_REQUEST: self.process_login_msg,
            MSG_LOGOUT_REQUEST: self.process_logout_msg,
        }
        if msg.msg_type in processors:
            processors[msg.msg_type](msg)

    def cleanup_connections(self, dead_connections :list[ServerConnection]):
        for connection in dead_connections:
            if connection in self.logged_users:
                self.logged_users.pop(connection)

    # TODO: Implement password hashing
    def process_login_msg(self, msg :LoginRequest):
        user = User.get_or_none(
            username = msg.username,
            password = msg.password
        )

        if self.is_logged(msg.owner) or self.is_user_logged(user):
            msg.owner.send(Response(
                msg.id,
                False,
                'Already logged in'
            ))
        elif not user:
            msg.owner.send(Response(
                msg.id,
                False,
                error_msg='User not found or invalid password', 
            ))
        else:
            self.logged_users[msg.owner] = user
            msg.owner.send(LoginInfo(True, msg.username, logged_in=True))
            msg.owner.send(Response(
                msg.id,
                True
            ))

    # TODO: make actual password/userame validation logic and password hashing
    def process_new_acc_msg(self, msg :CreateAccountRequest):
        if User.get_or_none(username=msg.username):
            msg.owner.send(Response(
                msg.id,
                False,
                error_str='User with that username already exists'
            ))
        elif self.is_logged(msg.owner):
            msg.owner.send(Response(
                msg.id,
                False,
                error_str='Cant create an account while logged in'
            ))
        else:
            user = User.create(
                username = msg.username,
                password = msg.password
            )
            self.logged_users[msg.owner] = user
            msg.owner.send(LoginInfo(True, msg.username, logged_in=True))
            msg.owner.send(Response(msg.id, True))

    def process_logout_msg(self, msg :LogoutRequest):
        if msg.owner in self.logged_users:
            self.logged_users.pop(msg.owner)
            msg.owner.send(LoginInfo(False, logged_out=True))
        msg.owner.send(Response(msg.id, True))
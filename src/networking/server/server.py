import select
import sys
import termios
import time
import tty
from networking.common import *
from . import *

class Server:
    connection_listener :ConnectionListener
    connection_manager :ConnectionManager
    login_manager :LoginManager
    room_manager :RoomManager

    def __init__(self):
        self.connection_listener = ConnectionListener()
        self.connection_listener.daemon = True
        self.connection_listener.start()
        self.connection_manager = ConnectionManager()
        self.login_manager = LoginManager()
        self.room_manager = RoomManager()

        time.sleep(0.1) # FIXME: Messy hack to wait for connection manager to properly initialize

    def run(self):
        try:
            while True:
                self.update()
        except KeyboardInterrupt:
            self.connection_listener.listener.close()
            time.sleep(0.3)
        except Exception as e:
            self.connection_listener.listener.close()
            time.sleep(0.3)
            raise e

    def update(self):
        self.accept_incoming_connections()
        self.process_messages()
        self.connection_manager.update()
        self.room_manager.update()
        self.cleanup_dead_connections()
        time.sleep(1/30)

    def accept_incoming_connections(self):
        while not self.connection_listener.new_connections.empty():
            conn = self.connection_listener.new_connections.get()
            self.connection_manager.add_connections(conn)

    def process_messages(self):
        while not self.connection_listener.in_queue.empty():
            msg = self.connection_listener.in_queue.get()
            self.connection_manager.process_message(msg)
            self.login_manager.process_message(msg)
            self.room_manager.process_message(msg)

    def cleanup_dead_connections(self):
        dead_connections = self.connection_manager.get_dead_connections()
        self.room_manager.cleanup(dead_connections)
        self.connection_manager.remove_dead_connections()

    def handle_keyboard(self):
        key = self._read_key()
        if key == 'c':
            self.connection_manager.kill_all()
        

    def _read_key(timeout=0.016):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                return sys.stdin.read(1)
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


    # def process_echo_request(self, msg :EchoRequest):
    #     msg.owner.out_queue.put(EchoResponse(f'{msg.echo_str}'))

    # def process_hello_msg(self, msg :Hello):
    #     print(f'Recieved connect form {msg.owner.conn}')

    # def process_clear_request(self, msg :ClearRequest):
    #     print(f'Dropping all connections...')
    #     for user in self.logged_users.keys():
    #         user.in_queue.put(LogoutResponse())
    #     time.sleep(0.5)
    #     self.connection_listener.clear_all()
    #     print(f'Done!')
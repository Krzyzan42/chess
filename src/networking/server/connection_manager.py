from networking.common import *

# Keeps track of alive connections
# Manages heartbeats and hello messages
# Responds to echo requests
class ConnectionManager:
    active_connections :list[Connection]
    _dead_connections :list[Connection]

    def __init__(self) -> None:
        self.active_connections = []
        self._dead_connections = []

    def add_connections(self, connection :Connection):
        self.active_connections.append(connection)

    def update(self):
        removed_conns = []
        for connection in self.active_connections:
            if not connection.is_alive():
                removed_conns.append(connection)
                print(f'Detected dead connection at {connection.address}. Removing')

        self._dead_connections += removed_conns
        for connection in removed_conns:
            self.active_connections.remove(connection)
        if len(removed_conns) > 0:
            print(f'Connections left: {len(self.active_connections)}')

    def process_message(self, msg :Message):
        if msg.msg_type == MSG_CLOSE:
            if msg.owner in self.active_connections:
                self.active_connections.remove(msg.owner)
                self._dead_connections.append(msg.owner)
                msg.owner.close()
                print(f'Recieved close message from {msg.owner.address}. Closing')
                print(f'Connections left: {len(self.active_connections)}')

    def get_dead_connections(self) -> list[Connection]:
        return self._dead_connections

    def remove_dead_connections(self):
        self._dead_connections = []

    def kill_all(self):
        print('Clearing all connections', flush=True)
        for conn in self.active_connections:
            conn.close()

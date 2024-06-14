from networking.common import *
import asyncio

# Keeps track of alive connections
# Manages heartbeats and hello messages
# Responds to echo requests
class ConnectionManager:
    active_connections :list[ServerConnection]
    _dead_connections :list[ServerConnection]

    def __init__(self) -> None:
        self.active_connections = []
        self._dead_connections = []

        asyncio.create_task(self.scan_for_dead_connections())
        asyncio.create_task(self.send_heartbeat_messages())

    def add_connection(self, connection :ServerConnection):
        self.active_connections.append(connection)

    async def scan_for_dead_connections(self):
        while True:
            removed_conns = []
            for conn in self.active_connections:
                if not conn.is_alive():
                    removed_conns.append(conn)

            self._dead_connections += removed_conns
            for conn in removed_conns:
                self.active_connections.remove(conn)
        
            await asyncio.sleep(1)

    async def send_heartbeat_messages(self):
        while True:
            for conn in self.active_connections:
                conn.send(HeartbeatMsg())
                await conn.drain()

            await asyncio.sleep(10)

    async def drain_all(self):
        for conn in self.active_connections:
            await conn.drain()

    def process_message(self, msg :Message):
        if msg.msg_type == MSG_CLOSE:
            raise NotImplementedError('Cant close the socket')

    def get_dead_connections(self) -> list[ServerConnection]:
        return self._dead_connections

    def remove_dead_connections(self):
        self._dead_connections = []
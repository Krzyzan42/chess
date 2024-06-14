import asyncio
from networking.common import ServerConnection
from networking.common.message import *
from networking.server import *
from networking import settings

class Server:
    msg_queue :asyncio.Queue
    connection_manager :ConnectionManager
    login_manager :LoginManager
    room_manager :RoomManager

    def __init__(self):
        self.msg_queue = asyncio.Queue()
        self.connection_manager = ConnectionManager()
        self.login_manager = LoginManager()
        self.room_manager = RoomManager()

    async def run(self):
        server = await asyncio.start_server(
            self._accept_connection, 
            settings.server_ip,
            settings.server_port
        )
        print(f'Hosting server on {settings.server_ip}:{settings.server_port}')
        self._serv = asyncio.create_task(server.serve_forever())

        while True:
            await self._update()

    async def _update(self):
        if self.msg_queue.qsize() > 0:
            msg = self.msg_queue.get_nowait()
            self.connection_manager.process_message(msg)
            self.login_manager.process_message(msg)
            self.room_manager.process_message(msg)

        self.room_manager.update()

        dead_conns = self.connection_manager.get_dead_connections()
        self.login_manager.cleanup_connections(dead_conns)
        self.connection_manager.remove_dead_connections()
        await self.connection_manager.drain_all()
        
        await asyncio.sleep(1/60)

    def _accept_connection(self, reader, writer):
        print('something happened')
        conn = ServerConnection(reader, writer, self.msg_queue)
        self.connection_manager.add_connection(conn)

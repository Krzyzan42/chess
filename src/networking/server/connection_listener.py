import socket
import networking.settings as settings
from queue import Queue
from threading import Thread
# from networking.common import Connection
from networking import settings

class ConnectionListener(Thread):
    new_connections :Queue
    in_queue :Queue
    listener :socket.socket

    def __init__(self):
        super().__init__()
        self.new_connections = Queue()

    def run(self):
        HOST = settings.server_ip
        PORT = settings.server_port
        self.in_queue = Queue()
        self.active_connections = []

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((HOST, PORT))
        self.listener.listen(5)
        while True:
            sock, addr = self.listener.accept()
            # connection = Connection(sock, in_queue=self.in_queue)
            # connection.address = addr
            # self.new_connections.put(connection)

            print(f'New connection accepted from {addr}')
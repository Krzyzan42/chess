from networking.common import *
import socket
from networking import settings

class TerminalClient:
    def __init__(self) -> None:
        self._server_port = settings.server_port
        self._server_ip = settings.server_ip

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._server_ip, self._server_port))
        self._connection = Connection(self._socket)

    def print_all_messages(self):
        print(self._connection.in_queue.qsize())
        print('-----------------------------')
        while not self._connection.in_queue.empty():
            msg = self._connection.in_queue.get()
            print(msg)
        print('-----------------------------')

    def send_msg(self, msg):
        self._connection.out_queue.put(msg)
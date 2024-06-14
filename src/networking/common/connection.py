import socket
import time
from queue import Queue
from . import *

class Connection:
    address :None

    def __init__(
                    self, 
                    conn :socket.socket, 
                    in_queue :Queue[Message] = None,
                    out_queue :Queue[Message] = None,
                 ):
        self.in_queue = in_queue if in_queue else Queue()
        self.out_queue = out_queue if out_queue else Queue()
        self.conn = conn

        self._setup_reader(conn, self.in_queue)
        self._setup_writer(conn, self.out_queue)
        
    def _setup_reader(self, conn :socket.socket, in_queue :Queue[Message]):
        self.reader = SocketReader()
        self.reader.conn = conn
        self.reader.incoming_messages = in_queue
        self.reader.daemon = True
        self.reader.owner = self
        self.reader.start()

    def _setup_writer(self, conn :socket.socket, out_queue :Queue[Message]):
        self.writer = SocketWriter()
        self.writer.conn = conn
        self.writer.outgoing_messages = out_queue
        self.writer.daemon = True
        self.writer.start()

    def is_alive(self):
        return self.writer.is_alive() and self.reader.is_alive()

    def check_timeout(self, max_timeout) -> bool:
        read_interval = time.time() - self.reader.last_read_time
        write_interval = time.time() - self.writer.last_write_time
        time_idle = min(read_interval, write_interval)

        if time_idle > max_timeout:
            self.close()
            return False

        return True

    def close(self):
        self.conn.close()

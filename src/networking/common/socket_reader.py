import socket
import pickle
import time
from threading import Thread
from queue import Queue
from logging import log, DEBUG
from networking.common import Message

class SocketReader(Thread):
    conn :socket.socket
    incoming_messages :Queue[Message]
    last_read_time :int
    owner = None

    def run(self):
        self.last_read_time = time.time()
        self.conn_alive = True
        self.left_data = b''

        try:
            while self.conn_alive:
                if not self.handle_read():
                    return
        except Exception as e:
            # return
            print('Error on read')
            print(e, flush=True)

    def handle_read(self) -> bool:
        data = self.left_data
        while len(data) < 4:
            recv_data = self.conn.recv(1024)
            if len(recv_data) == 0:
                self.conn.close()
                return False
            data += recv_data

        payload_size = int.from_bytes(data[:4], 'big')
        data = data[4:]

        while len(data) < payload_size:
            recv_data = self.conn.recv(1024)
            if len(recv_data) == 0:
                self.conn.close()
                return False
            data += recv_data

        payload_data = data[:payload_size]
        msg_body :Message = pickle.loads(payload_data)
        msg_body.owner = self.owner
        self.left_data = data[payload_size:]
        
        log(DEBUG, f'Read {msg_body}')
        self.incoming_messages.put(msg_body)
        self.last_read_time = time.time()

        return True
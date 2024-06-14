import socket
import pickle
from threading import Thread
from queue import Queue, Empty
from logging import log, DEBUG
from networking.common import Message

class SocketWriter(Thread):
    conn :socket.socket
    outgoing_messages :Queue[Message]
    last_write_time :int

    def run(self):
        self.conn_alive = True
        try:
            while self.conn_alive:
                self.handle_write()
        except Exception as e:
            # return
            print('error on write')
            print(str(e), flush=True)

        # print('Thread exiting peacfully')
    
    # Timeout must be here, otherwise after the connection gets killed,
    # the thread might be left hanging without encountering exception on
    # the sendall
    def handle_write(self):
        message = None
        try:
            message = self.outgoing_messages.get(timeout=1)
        except Empty:
            return

        msg_payload = pickle.dumps(message)
        
        bytes_sent = int.to_bytes(len(msg_payload), 4, 'big')
        bytes_sent += msg_payload

        self.conn.sendall(bytes_sent)
        log(DEBUG, f'Sent {message}')
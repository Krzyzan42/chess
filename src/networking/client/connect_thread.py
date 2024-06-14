from PySide6.QtCore import *
from PySide6.QtCore import QObject
import socket
import time

class ConnectThread(QThread):
    result_ready = Signal(bool, str)

    ip_address :str
    port :int

    result_socket :socket.socket

    def __init__(self, ip_address :str = None, port :int = None):
        super().__init__()
        self.ip_address = ip_address
        self.port = port

    def run(self):
        time.sleep(0.5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ip_address, self.port))
        except Exception as e:
            self.result_socket = None
            s.close()
            self.result_ready.emit(False, str(e))
        else:
            self.result_socket = s
            self.result_ready.emit(True, None)
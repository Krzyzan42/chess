class SocketError(Exception):
    reason :str

    def __init__(self, reason :str = None):
        self.reason = reason if reason else 'Unknown'